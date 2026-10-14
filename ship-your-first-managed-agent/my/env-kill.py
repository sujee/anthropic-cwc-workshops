# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""
Experiment: what happens when an environment is deleted mid-session?

Starts a long-running task, deletes the environment N seconds in, and logs
every event, error and state change with timestamps.

    python my/env-kill.py --kill-after 10
"""
import argparse
import threading
import time
import uuid

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-5-5"

PROMPT = """\
Use bash to run this exact command and report when it finishes:
for i in $(seq 1 {ticks}); do echo "tick $i"; sleep 2; done
"""

FOLLOW_UP = "Use bash to run `echo hello from after the kill; uname -n` and show the output."

client = anthropic.Anthropic()
t0 = time.time()


def log(msg: str) -> None:
    print(f"[{time.time() - t0:6.1f}s] {msg}", flush=True)


def kill_env(env_id: str) -> None:
    log(f"!! deleting environment {env_id}")
    try:
        client.beta.environments.delete(env_id)
        log("!! environment delete returned OK")
    except Exception as e:
        log(f"!! environment delete failed: {type(e).__name__}: {e}")


def run_turn(session_id: str, text: str, label: str, on_open=None) -> None:
    """Send a message, log every event until idle (or error)."""
    try:
        with client.beta.sessions.events.stream(session_id) as stream:
            client.beta.sessions.events.send(
                session_id,
                events=[{"type": "user.message", "content": [{"type": "text", "text": text}]}],
            )
            if on_open:
                on_open()
            for event in stream:
                detail = getattr(event, "name", "")
                log(f"{label} event: {event.type} {detail}")
                if event.type == "agent.tool_result":
                    out = str(getattr(event, "content", ""))
                    log(f"{label}   tool_result ({len(out)} chars): {out[:150]!r} ... {out[-100:]!r}")
                elif event.type == "agent.message":
                    log(f"{label}   message: {str(event.content)[:300]}")
                if event.type == "session.status_idle":
                    break
    except Exception as e:
        log(f"{label} stream error: {type(e).__name__}: {e}")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kill-after", type=float, default=10, help="seconds before deleting the env")
    ap.add_argument("--ticks", type=int, default=60, help="loop iterations (2s each) in the long task")
    args = ap.parse_args()

    env = client.beta.environments.create(
        name=f"env-kill-{uuid.uuid4().hex[:6]}",
        config={"type": "cloud", "networking": {"type": "limited"}},
    )
    agent = client.beta.agents.create(
        name=f"env-kill-{uuid.uuid4().hex[:6]}",
        model=MODEL,
        system="You are a sysadmin. Run commands exactly as asked.",
        tools=[{"type": "agent_toolset_20260401"}],
    )
    session = client.beta.sessions.create(
        agent=agent.id, environment_id=env.id, title="env-kill experiment"
    )
    log(f"env={env.id} session={session.id}; killing env in {args.kill_after}s")

    run_turn(
        session.id,
        PROMPT.format(ticks=args.ticks),
        "main",
        on_open=lambda: threading.Timer(args.kill_after, kill_env, args=(env.id,)).start(),
    )

    # Aftermath: what state is the session in, and can we still talk to it?
    try:
        s = client.beta.sessions.retrieve(session.id)
        log(f"session after kill: status={getattr(s, 'status', '?')}")
    except Exception as e:
        log(f"session retrieve failed: {type(e).__name__}: {e}")

    log("sending follow-up turn that needs a sandbox...")
    run_turn(session.id, FOLLOW_UP, "follow-up")

    try:
        client.beta.sessions.delete(session.id)
        log("session deleted")
    except Exception as e:
        log(f"session delete failed: {type(e).__name__}: {e}")


if __name__ == "__main__":
    main()
