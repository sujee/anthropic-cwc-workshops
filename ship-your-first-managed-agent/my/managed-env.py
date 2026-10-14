# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""
Create a Managed Agents cloud environment and print what's inside it
(OS version, CPU, memory, disks).

An environment is only a config until a session runs in it, so we start a
throwaway session and have the agent run the inspection commands in the sandbox.
"""
import json
import uuid

import anthropic
from dotenv import load_dotenv

load_dotenv()  # reads ANTHROPIC_API_KEY from .env

MODEL = "claude-sonnet-5-5"

PROMPT = """\
Inspect the sandbox you are running in. Use bash to run these commands:
  cat /etc/os-release; uname -a
  lscpu; nproc
  free -h
  df -h; lsblk
Then reply with ONLY a JSON object (no prose, no code fence) shaped like:
{"os": {"name": "", "version": "", "kernel": "", "arch": ""},
 "cpu": {"model": "", "cores": 0},
 "memory": {"total": "", "used": "", "free": ""},
 "disks": [{"filesystem": "", "size": "", "used": "", "avail": "", "mount": ""}]}
Use the actual values. Include only real disks/mounts (skip tmpfs, overlay noise
unless it is the root filesystem).
"""

client = anthropic.Anthropic()


def print_report(raw: str) -> None:
    """Print the agent's JSON report indented; fall back to the raw text."""
    try:
        print(json.dumps(json.loads(raw[raw.index("{") : raw.rindex("}") + 1]), indent=2))
    except ValueError:
        print(raw)


# 1. Environment: where the agent's container runs.
env = client.beta.environments.create(
    name=f"env-inspect-{uuid.uuid4().hex[:6]}",
    config={"type": "cloud", "networking": {"type": "limited"}},
)
print(f"Environment created: {env.id}")

# 2. Agent: minimal, with the built-in toolset (bash, file ops, ...).
agent = client.beta.agents.create(
    name=f"env-inspector-{uuid.uuid4().hex[:6]}",
    model=MODEL,
    system="You are a sysadmin. Run commands and report their real output.",
    tools=[{"type": "agent_toolset_20260401"}],
)

# 3. Session: boots the sandbox from the environment config.
session = client.beta.sessions.create(
    agent=agent.id,
    environment_id=env.id,
    title="Inspect environment",
)
print(f"Session started: {session.id}\n")

try:
    reply = ""
    with client.beta.sessions.events.stream(session.id) as stream:
        client.beta.sessions.events.send(
            session.id,
            events=[
                {
                    "type": "user.message",
                    "content": [{"type": "text", "text": PROMPT}],
                }
            ],
        )
        for event in stream:
            match event.type:
                case "agent.message":
                    for block in event.content:
                        if block.type == "text":
                            reply += block.text
                case "agent.tool_use":
                    print(f"[running tool: {event.name}]")
                case "session.status_idle":
                    break
    print_report(reply)
finally:
    # Sessions are real cloud resources — clean up.
    client.beta.sessions.delete(session.id)
    print(f"Session {session.id} deleted (environment {env.id} kept for reuse).")
