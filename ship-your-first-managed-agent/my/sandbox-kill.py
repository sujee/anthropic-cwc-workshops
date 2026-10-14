# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""
Experiment: if the sandbox dies mid-session, does a new one start automatically?

Each sandbox is a fresh filesystem, so a marker file tells us which sandbox we are in.

  turn 1  write /tmp/marker-<id>, record hostname, PID 1 start time and uptime
  turn 2  kill the sandbox from inside (the environment config stays in place)
  turn 3  look for the marker and record the same fingerprint again

  marker present, same fingerprint     same sandbox: the kill did not take
  marker missing, command works        a NEW sandbox started automatically
  turn 3 errors, hangs or terminates   no automatic restart

    python my/sandbox-kill.py                      # kill -9 -1 (every process we may signal)
    python my/sandbox-kill.py --method init        # kill -9 1
    python my/sandbox-kill.py --method none        # control: no kill, expect "same sandbox"
    python my/sandbox-kill.py --delete-env         # also delete the environment first
"""
import argparse
import re
import threading
import time
import uuid

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-5-5"
KILL = {
    "killall": "kill -9 -1",
    "init": "kill -9 1",
    "none": "echo no-kill control",
}

# Prints KEY=value lines we can parse, whatever the agent says afterwards.
FINGERPRINT = (
    'echo HOST=$(hostname); '
    'echo PID1=$(stat -c %Y /proc/1 2>/dev/null || ps -o lstart= -p 1); '
    'echo UPTIME=$(cut -d" " -f1 /proc/uptime)'
)

client = anthropic.Anthropic()
t0 = time.time()


def log(msg: str) -> None:
    print(f"[{time.time() - t0:6.1f}s] {msg}", flush=True)


def run_turn(session_id: str, text: str, label: str, timeout: float = 120) -> dict:
    """Send a message and log every event. Never raises.

    Returns {"out": tool_result text, "tool_used": did the agent call a tool,
             "said": the agent's text, "failed": error, terminated or no idle}.
    """
    results: list[str] = []
    said: list[str] = []
    turn = {"tool_used": False, "failed": False}
    try:
        with client.beta.sessions.events.stream(session_id) as stream:
            # A killed sandbox may never answer, so close the stream at the deadline.
            watchdog = threading.Timer(timeout, stream.close)
            watchdog.start()
            try:
                client.beta.sessions.events.send(
                    session_id,
                    events=[{"type": "user.message", "content": [{"type": "text", "text": text}]}],
                )
                for event in stream:
                    log(f"{label} event: {event.type} {getattr(event, 'name', '')}")
                    if event.type == "agent.tool_use":
                        turn["tool_used"] = True
                        log(f"{label}   command: {getattr(event, 'input', '')!r}"[:300])
                    elif event.type == "agent.tool_result":
                        out = "".join(getattr(b, "text", "") for b in event.content)
                        results.append(out)
                        log(f"{label}   tool_result: {out.strip()[:300]!r}")
                    elif event.type == "agent.message":
                        msg = "".join(getattr(b, "text", "") for b in event.content)
                        said.append(msg)
                        log(f"{label}   agent said: {msg.strip()[:400]!r}")
                    elif event.type == "session.error":
                        turn["failed"] = True
                        log(f"{label}   session.error: {event!r}"[:600])
                    if event.type == "session.status_terminated":
                        turn["failed"] = True
                    if event.type in ("session.status_idle", "session.status_terminated"):
                        break
                else:
                    turn["failed"] = True
                    log(f"{label} stream ended with no idle (closed by watchdog or server)")
            finally:
                watchdog.cancel()
    except Exception as e:
        turn["failed"] = True
        log(f"{label} stream error: {type(e).__name__}: {e}")
    return {**turn, "out": "\n".join(results), "said": "\n".join(said)}


def parse(text: str) -> dict:
    return dict(re.findall(r"^(MARKER|HOST|PID1|UPTIME)=(.*)$", text, re.M))


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--method", choices=list(KILL), default="killall")
    ap.add_argument("--delete-env", action="store_true", help="also delete the environment before turn 3")
    args = ap.parse_args()

    env = client.beta.environments.create(
        name=f"sbx-kill-{uuid.uuid4().hex[:6]}",
        config={"type": "cloud", "networking": {"type": "limited"}},
    )
    agent = client.beta.agents.create(
        name=f"sbx-kill-{uuid.uuid4().hex[:6]}",
        model=MODEL,
        system=(
            "You are a sysadmin working in a disposable test sandbox that exists only for "
            "this experiment. Nothing in it matters and the operator has authorized every "
            "command, including ones that kill processes or crash the sandbox. Run each "
            "command exactly as given, in bash, and show its output."
        ),
        tools=[{"type": "agent_toolset_20260401"}],
    )
    session = client.beta.sessions.create(
        agent=agent.id, environment_id=env.id, title="sandbox-kill experiment"
    )
    marker = f"/tmp/marker-{uuid.uuid4().hex[:8]}"
    log(f"env={env.id} session={session.id} marker={marker} method={args.method}")

    try:
        # Turn 1: baseline.
        log("TURN 1: write marker, record fingerprint")
        t1 = run_turn(
            session.id,
            f'Run exactly this in bash: echo {marker} > {marker}; {FINGERPRINT}',
            "t1",
        )
        before = parse(t1["out"])
        log(f"baseline: {before}")

        # Turn 2: kill the sandbox from inside.
        log(f"TURN 2: kill the sandbox ({KILL[args.method]})")
        t2 = run_turn(session.id, f"Run exactly this in bash: {KILL[args.method]}", "t2", timeout=60)
        s = client.beta.sessions.retrieve(session.id)
        log(f"session status after kill: {getattr(s, 'status', '?')}")

        if args.delete_env:
            log("!! also deleting the environment")
            try:
                client.beta.environments.delete(env.id)
                log("environment delete returned OK")
            except Exception as e:
                log(f"environment delete failed: {type(e).__name__}: {e}")

        # Turn 3: what is there now?
        log("TURN 3: look for the marker, record fingerprint")
        t3 = run_turn(
            session.id,
            f'Run exactly this in bash: if [ -f {marker} ]; then echo MARKER=present; '
            f'else echo MARKER=missing; fi; {FINGERPRINT}',
            "t3",
        )
        after = parse(t3["out"])
        log(f"after: {after}")

        # Verdict. A turn where the agent never ran a command proves nothing about the sandbox.
        print("\n" + "=" * 60)
        if not t1["tool_used"] or not before:
            print("INCONCLUSIVE: the baseline turn did not run, so there is nothing to compare with.")
        elif args.method != "none" and not t2["tool_used"]:
            print("INCONCLUSIVE: the kill never ran. The agent did not call bash in turn 2.")
            print(f"  agent said: {t2['said'].strip()[:300]!r}")
        elif t3["failed"]:
            print("NO AUTOMATIC RESTART observed: turn 3 errored, hung or the session terminated.")
            print("  see the session.error and status events above.")
        elif not t3["tool_used"] or not after:
            print("INCONCLUSIVE: the agent did not run the turn 3 check, so the sandbox was not tested.")
            print(f"  agent said: {t3['said'].strip()[:300]!r}")
        elif after.get("MARKER") == "present":
            same = after.get("PID1") == before.get("PID1")
            print(f"SAME sandbox (marker present, PID 1 start {'unchanged' if same else 'CHANGED'}).")
            if args.method == "none":
                print("  expected for the control: nothing was killed.")
            else:
                print("  the kill ran but the sandbox kept its files: it was not replaced.")
        else:
            print("NEW sandbox started automatically (marker missing, commands still work).")
            print(f"  PID 1 start {before.get('PID1')} -> {after.get('PID1')}, "
                  f"uptime {before.get('UPTIME')} -> {after.get('UPTIME')}")
        print("=" * 60)
    finally:
        try:
            client.beta.sessions.delete(session.id)
            log("session deleted")
        except Exception as e:
            log(f"session delete failed: {type(e).__name__}: {e}")
        log(f"left behind for reuse: env={env.id} agent={agent.id}")


if __name__ == "__main__":
    main()
