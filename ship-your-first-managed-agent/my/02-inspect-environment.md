# 02 · Inspect the environment

[Back to README](README.md) · Previous: [01 · Getting started](01-getting-started.md) · Next: [03 · Kill experiments](03-kill-experiments.md)

**Why.** I wanted a deeper understanding of managed environments: what is actually inside one?

**Script:** [managed-env.py](managed-env.py)

## The catch

An environment on its own is only a stored setting. It has no shell, so you cannot ask it about its OS or memory. To look inside, the script has to create a throwaway agent and a session, and have the agent run bash in the sandbox.

## The prompt I gave Claude

```
Write managed-env.py using the Anthropic Python SDK's Managed Agents beta
(https://platform.claude.com/docs/en/managed-agents/quickstart).

- Load ANTHROPIC_API_KEY from .env (python-dotenv).
- Create a cloud environment and print its ID.
- Then start a throwaway agent (agent_toolset_20260401,
claude-sonnet-5-5) and session in it,
- and have the agent run bash to inspect the sandbox and reply with only JSON: os, cpu, memory, disks.
- Stream until session.status_idle, print the JSON indented,
- then delete the session.
```

## Run it

From the project folder:

```bash
source .venv/bin/activate
pip install -r requirements.txt

python my/managed-env.py
```

Then look at what it created in the console: [Agents](https://platform.claude.com/workspaces/default/agents-overview) | [Sessions](https://platform.claude.com/workspaces/default/sessions) | [Environments](https://platform.claude.com/workspaces/default/environments)

## What I learned

- The environment, the agent and the session are three separate objects. The script creates all three, and only the session runs anything. (See the [slides](07-slides.md), section "Understanding managed agents".)
- The sandbox boots on demand. In later runs, the machine's uptime was only about 5 seconds when the first command ran.
- The script deletes the session but leaves the environment and agent behind. Every run adds to what [04 · Resources](04-resources.md) has to clean up.

## Next

Once I could see inside one, the obvious question was what happens when you pull it out from under a running session. That is [03](03-kill-experiments.md).

---

[Back to README](README.md) · Previous: [01 · Getting started](01-getting-started.md) · Next: [03 · Kill experiments](03-kill-experiments.md)
