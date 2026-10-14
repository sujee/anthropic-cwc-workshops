# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""
Clean up the cloud resources left behind by the experiment scripts.

Only touches resources whose name starts with one of the prefixes below, so the
workshop's own resources ("SRE Agent", "sre-agent-...") are never listed.
It is a dry run unless you pass --yes.

    python my/cleanup.py            # list what would be removed
    python my/cleanup.py --yes      # remove it

Order matters: deployments first (stops new sessions), then sessions, then
environments (they cannot be deleted while sessions reference them), then agents.
"""
import argparse

import anthropic
from dotenv import load_dotenv

load_dotenv()

PREFIXES = ("env-kill-", "dep-kill-", "sbx-kill-", "env-inspect-", "env-inspector-", "anim-capture-")

client = anthropic.Anthropic()


def ours(name: str | None) -> bool:
    return bool(name) and name.startswith(PREFIXES)


def attempt(label: str, fn) -> bool:
    try:
        fn()
        print(f"  removed  {label}")
        return True
    except Exception as e:
        print(f"  FAILED   {label}: {type(e).__name__}: {e}")
        return False


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--yes", action="store_true", help="actually remove (default is a dry run)")
    args = ap.parse_args()

    # Find our resources.
    deployments = [d for d in client.beta.deployments.list() if ours(d.name)]
    envs = [e for e in client.beta.environments.list() if ours(e.name)]
    agents = [a for a in client.beta.agents.list() if ours(a.name)]
    env_ids = {e.id for e in envs}
    agent_ids = {a.id for a in agents}
    sessions = [
        s for s in client.beta.sessions.list()
        if getattr(s, "environment_id", None) in env_ids
        or getattr(getattr(s, "agent", None), "id", None) in agent_ids
    ]

    print(f"deployments: {len(deployments)}  sessions: {len(sessions)}  "
          f"environments: {len(envs)}  agents: {len(agents)}")
    for kind, items in (("deployment", deployments), ("session", sessions),
                        ("environment", envs), ("agent", agents)):
        for x in items:
            print(f"  {kind:<12}{x.id}  {getattr(x, 'name', None) or getattr(x, 'title', '') or ''}")

    if not args.yes:
        print("\nDry run. Re-run with --yes to remove these.")
        return

    print()
    done = failed = 0
    steps = (
        [(f"deployment {d.id}", lambda d=d: client.beta.deployments.archive(d.id)) for d in deployments]
        + [(f"session {s.id}", lambda s=s: client.beta.sessions.delete(s.id)) for s in sessions]
        + [(f"environment {e.id}", lambda e=e: client.beta.environments.delete(e.id)) for e in envs]
        + [(f"agent {a.id}", lambda a=a: client.beta.agents.archive(a.id)) for a in agents]
    )
    for label, fn in steps:
        if attempt(label, fn):
            done += 1
        else:
            failed += 1
    print(f"\n{done} removed, {failed} failed. (Deployments and agents are archived, not deleted.)")


if __name__ == "__main__":
    main()
