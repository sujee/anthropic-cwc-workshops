# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""
Experiment: what happens when a scheduled deployment is terminated?

Creates a deployment that fires every minute and starts a long-running session.
Once the first session is up, it archives (or pauses) the deployment and then
keeps watching: does the running session finish? do more runs fire? what state
does the deployment end up in?

    python my/deployment-kill.py --kill archive --kill-after 20
    python my/deployment-kill.py --kill pause
    python my/deployment-kill.py --kill none        # control: let it fire, then clean up
"""
import argparse
import time
import uuid

import anthropic
from dotenv import load_dotenv

load_dotenv()

MODEL = "claude-sonnet-5-5"

TASK = """\
Use bash to run this exact command and report when it finishes:
for i in $(seq 1 {ticks}); do echo "tick $i"; sleep 2; done
"""

client = anthropic.Anthropic()
t0 = time.time()


def log(msg: str) -> None:
    print(f"[{time.time() - t0:6.1f}s] {msg}", flush=True)


def attempt(label: str, fn):
    """Run fn, log the outcome, never raise: errors are the data."""
    try:
        out = fn()
        log(f"{label}: OK")
        return out
    except Exception as e:
        log(f"{label}: {type(e).__name__}: {e}")
        return None


def snapshot(dep_id: str, seen_sessions: dict) -> list:
    """Log deployment status, every run, and the status of every session started."""
    d = client.beta.deployments.retrieve(dep_id)
    log(f"deployment status={d.status} paused_reason={getattr(d, 'paused_reason', None)}")
    runs = list(client.beta.deployment_runs.list(deployment_id=dep_id))
    for r in runs:
        sid = getattr(r, "session_id", None)
        err = getattr(r, "error", None)
        if sid and sid not in seen_sessions:
            log(f"  new run {r.id}: session={sid}")
            seen_sessions[sid] = None
        elif err:
            log(f"  run {r.id}: ERROR {err.type}: {err.message}")
    for sid in seen_sessions:
        s = client.beta.sessions.retrieve(sid)
        if s.status != seen_sessions[sid]:
            log(f"  session {sid}: status={s.status}")
            seen_sessions[sid] = s.status
    return runs


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--kill", choices=["archive", "pause", "none"], default="archive")
    ap.add_argument("--kill-after", type=float, default=20, help="seconds after the first session appears")
    ap.add_argument("--watch", type=float, default=240, help="seconds to keep watching after the kill")
    ap.add_argument("--ticks", type=int, default=60, help="2s ticks in the long task (60 = 2 min)")
    args = ap.parse_args()

    env = client.beta.environments.create(
        name=f"dep-kill-{uuid.uuid4().hex[:6]}",
        config={"type": "cloud", "networking": {"type": "limited"}},
    )
    agent = client.beta.agents.create(
        name=f"dep-kill-{uuid.uuid4().hex[:6]}",
        model=MODEL,
        system="You are a sysadmin. Run commands exactly as asked.",
        tools=[{"type": "agent_toolset_20260401"}],
    )
    dep = client.beta.deployments.create(
        name=f"dep-kill-{uuid.uuid4().hex[:6]}",
        agent=agent.id,
        environment_id=env.id,
        initial_events=[
            {
                "type": "user.message",
                "content": [{"type": "text", "text": TASK.format(ticks=args.ticks)}],
            }
        ],
        schedule={"type": "cron", "expression": "* * * * *", "timezone": "UTC"},
    )
    log(f"env={env.id} agent={agent.id} deployment={dep.id}")
    log(f"next fires: {dep.schedule.upcoming_runs_at[:3]}")

    seen: dict = {}
    try:
        # Phase 1: wait for the first scheduled fire to start a session.
        while not seen:
            time.sleep(5)
            snapshot(dep.id, seen)
            if time.time() - t0 > 240:
                log("no run after 4 minutes, giving up")
                return

        # Phase 2: the kill.
        time.sleep(args.kill_after)
        if args.kill == "archive":
            log("!! archiving deployment (terminal)")
            attempt("deployments.archive", lambda: client.beta.deployments.archive(dep.id))
        elif args.kill == "pause":
            log("!! pausing deployment")
            attempt("deployments.pause", lambda: client.beta.deployments.pause(dep.id))
        else:
            log("control: no kill")

        # Phase 3: watch the aftermath.
        end = time.time() + args.watch
        while time.time() < end:
            snapshot(dep.id, seen)
            time.sleep(10)

        # Phase 4: can the deployment still be used?
        attempt("manual run after kill", lambda: client.beta.deployments.run(dep.id))
        attempt("update after kill", lambda: client.beta.deployments.update(dep.id, name="renamed"))
        if args.kill == "pause":
            attempt("unpause", lambda: client.beta.deployments.unpause(dep.id))
    finally:
        attempt("final archive", lambda: client.beta.deployments.archive(dep.id))
        for sid in seen:
            attempt(f"delete session {sid}", lambda sid=sid: client.beta.sessions.delete(sid))
        log(f"left behind for reuse: env={env.id} agent={agent.id}")


if __name__ == "__main__":
    main()
