# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""
List every Managed Agents resource in your account as a tree. Read-only.

    agent
    └── environment it ran in
        ├── session
        └── deployment

    python my/list-resources.py
"""
import anthropic
from dotenv import load_dotenv

load_dotenv()

client = anthropic.Anthropic()


def ref_id(x):
    """An id, whether the SDK gives a string or an object with .id."""
    return x if isinstance(x, str) or x is None else getattr(x, "id", None)


def when(x) -> str:
    return str(getattr(x, "created_at", "") or "")[:19].replace("T", " ")


def children(lines: list[str], prefix: str) -> None:
    for i, line in enumerate(lines):
        print(f"{prefix}{'└── ' if i == len(lines) - 1 else '├── '}{line}")


def main() -> None:
    agents = list(client.beta.agents.list())
    envs = {e.id: e for e in client.beta.environments.list()}
    sessions = list(client.beta.sessions.list())
    deployments = list(client.beta.deployments.list())

    # agent id -> env id -> {"sessions": [...], "deployments": [...]}
    tree: dict = {a.id: {} for a in agents}
    seen_envs = set()

    def slot(agent_id, env_id):
        seen_envs.add(env_id)
        return tree.setdefault(agent_id, {}).setdefault(env_id, {"sessions": [], "deployments": []})

    for s in sessions:
        slot(ref_id(s.agent), s.environment_id)["sessions"].append(
            f"session     {s.id}  {s.status}  {getattr(s, 'title', None) or ''}  {when(s)}")
    for d in deployments:
        slot(ref_id(d.agent), d.environment_id)["deployments"].append(
            f"deployment  {d.id}  {getattr(d, 'status', '')}  {d.name}")

    names = {a.id: a for a in agents}
    for agent_id, by_env in tree.items():
        a = names.get(agent_id)
        print(f"agent  {agent_id}  {getattr(a, 'name', '(deleted)')}  v{getattr(a, 'version', '?')}  {when(a) if a else ''}")
        env_ids = list(by_env)
        for i, env_id in enumerate(env_ids):
            last = i == len(env_ids) - 1
            e = envs.get(env_id)
            print(f"{'└── ' if last else '├── '}environment  {env_id}  {e.name if e else '(deleted)'}")
            children(by_env[env_id]["sessions"] + by_env[env_id]["deployments"], "    " if last else "│   ")
        if by_env:
            print()

    unused = [e for e in envs.values() if e.id not in seen_envs]
    if unused:
        print("environments with no sessions or deployments")
        children([f"environment  {e.id}  {e.name}  {when(e)}" for e in unused], "")
        print()

    print(f"{len(agents)} agents, {len(envs)} environments, {len(sessions)} sessions, {len(deployments)} deployments")


if __name__ == "__main__":
    main()
