# Copyright 2026 Anthropic PBC
# SPDX-License-Identifier: Apache-2.0
"""
Run the SRE agent once, headless, and save every event with its timing.

The animated page replays this file, so the animation shows what really happened
instead of an invented sequence.

    python my/capture-events.py            # writes my/run-events.json
"""
import json
import os
import sys
import time
import uuid
from pathlib import Path

import anthropic
from anthropic.lib import files_from_dir
from dotenv import load_dotenv

# This script lives in my/. provided.py and data/ live one level up, and provided.py
# reads data/ relative to the working directory, so run from the project root.
ROOT = Path(__file__).resolve().parent.parent
sys.path.insert(0, str(ROOT))
os.chdir(ROOT)

from provided import MODEL, SYSTEM, TOOLS, deploys, diff, metrics  # noqa: E402

load_dotenv()
OUT = Path(__file__).resolve().parent / "run-events.json"
QUESTION = "checkout p99 spiked ~14:32 UTC. What caused it?"

client = anthropic.Anthropic()


def handle(name: str, args: dict) -> str:
    if name == "get_metrics":
        return json.dumps(metrics.get(args["service"], {}).get(args["metric"]) or {"error": "not found"})
    if name == "get_recent_deploys":
        return deploys
    if name == "get_diff":
        return diff if args["commit"][:7] in diff else "no diff for that commit"
    return f"unknown tool {name}"


def trim(x, n=500):
    """Shorten long strings anywhere in a nested structure, so the file stays small."""
    if isinstance(x, str):
        return x if len(x) <= n else x[:n] + f"... [{len(x)} chars]"
    if isinstance(x, list):
        return [trim(i, n) for i in x]
    if isinstance(x, dict):
        return {k: trim(v, n) for k, v in x.items()}
    return x


def main() -> None:
    tag = f"anim-capture-{uuid.uuid4().hex[:6]}"
    skill = client.beta.skills.create(
        display_name=f"{tag} runbook",
        files=files_from_dir(ROOT / "incident-triage-runbook"),
    )
    agent = client.beta.agents.create(
        name=tag, model=MODEL, system=SYSTEM, tools=TOOLS,
        skills=[{"type": "custom", "skill_id": skill.id, "version": "latest"}],
    )
    env = client.beta.environments.create(
        name=tag, config={"type": "cloud", "networking": {"type": "limited"}},
    )
    with open(ROOT / "data" / "app.log", "rb") as f:
        log = client.beta.files.upload(file=f)
    session = client.beta.sessions.create(
        agent=agent.id, environment_id=env.id,
        resources=[{"type": "file", "file_id": log.id, "mount_path": "app.log"}],
    )
    print(f"agent={agent.id} env={env.id} session={session.id}", flush=True)

    events = []
    t0 = time.time()

    def record(source: str, ev) -> None:
        raw = ev.model_dump(mode="json") if hasattr(ev, "model_dump") else dict(ev)
        # Keep the agent's answer whole; shorten everything else.
        d = trim(raw, 4000 if raw.get("type") == "agent.message" else 700)
        events.append({"t": round(time.time() - t0, 2), "source": source, **d})
        print(f"[{time.time() - t0:6.1f}s] {source:<6} {d.get('type')} {d.get('name', '')}", flush=True)

    with client.beta.sessions.events.stream(session.id) as stream:
        msg = {"type": "user.message", "content": [{"type": "text", "text": QUESTION}]}
        client.beta.sessions.events.send(session.id, events=[msg])
        events.append({"t": 0.0, "source": "you", **msg})
        print(f"[   0.0s] you    user.message", flush=True)
        for ev in stream:
            record("agent", ev)
            if ev.type == "agent.custom_tool_use":
                result = handle(ev.name, ev.input)
                reply = {"type": "user.custom_tool_result", "custom_tool_use_id": ev.id,
                         "content": [{"type": "text", "text": result}]}
                client.beta.sessions.events.send(session.id, events=[reply])
                events.append({"t": round(time.time() - t0, 2), "source": "you", **trim(reply)})
                print(f"[{time.time() - t0:6.1f}s] you    user.custom_tool_result ({len(result)} chars)", flush=True)
            elif ev.type == "session.status_idle" and ev.stop_reason.type == "end_turn":
                break
            if time.time() - t0 > 600:
                print("!! timeout", flush=True)
                break

    OUT.write_text(json.dumps({"question": QUESTION, "model": MODEL, "events": events}, indent=1))
    print(f"saved {len(events)} events to {OUT}", flush=True)
    print(f"to remove: python my/cleanup.py (prefix anim-capture-)", flush=True)
    client.beta.sessions.delete(session.id)


if __name__ == "__main__":
    main()
