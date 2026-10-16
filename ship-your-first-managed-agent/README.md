<!-- Copyright 2026 Anthropic PBC -->
<!-- SPDX-License-Identifier: Apache-2.0 -->

# Ship Your First Managed Agent — Incident-2277

## Quick links

- **[Lab notes](my/lab-notes.md):** start building here
- **[My work](my/README.md):** my exploration notes, slides, animation and tutor

---

> **Workshop sample.** Not maintained and not accepting contributions.

> **It's 2am. PagerDuty fires: checkout p99 latency is 10× baseline.**
> You know the drill — open the dashboard, grep logs, scroll deploys, guess,
> check, repeat. Forty minutes later you find it: someone shipped an N+1 query.
>
> This workshop builds the agent that does that forty minutes for you.

A working incident dashboard for a fictional e-commerce stack. The Metrics,
Logs, and Deploys pages run out of the box from mock data. There's an
**SRE Agent** chat panel on the side of every page — and it's offline.
Bringing it online is the workshop: seven small functions in one file, each a
single [Claude Managed Agents](https://platform.claude.com/docs/en/managed-agents/overview)
API call.

When you're done, you ask it *"what caused the latency spike?"* and watch it
grep a 70k-line log inside its own cloud sandbox, call your local tools to
pull metrics and deploys, correlate the timestamps, fetch the offending diff,
and name the commit.

## What you build

By the end you'll have an SRE agent that:

- **Runs in a managed cloud sandbox:** it greps and analyzes a 70k-line log with Python you never deploy
- **Calls tools on your laptop:** `get_metrics`, `get_recent_deploys` and `get_diff`, over the event stream
- **Follows your team's runbook:** an uploaded skill keeps every investigation consistent
- **Names the root cause:** it correlates the latency spike with a deploy and points to the bad commit


## The incident

`data/` ships a real-feeling outage: at **14:31:18 UTC** commit `a3f9c21`
deploys to the checkout service, replacing a batched query with a per-row
loop. Within minutes p99 latency climbs from 65 ms to 3,600 ms, the DB
connection pool saturates, and 20% of checkouts start failing.

The evidence is spread across:

- `app.log` — 70,000 lines of JSON logs the agent has to grep in its sandbox
- `metrics.json` / `deploys.json` / `diff.txt` — what `get_metrics`,
  `get_recent_deploys`, and `get_diff` return when the agent calls them
  (these handlers run on **your** machine, not the cloud — that's the point)

The agent has to correlate all four to name the root cause. It does.

## What this teaches

- **Agent → Environment → Session → Events** — the four Managed Agents
  resources, in the order the
  [quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart)
  introduces them
- **Skills** — `incident-triage-runbook/SKILL.md` packages this team's runbook;
  uploaded and attached inside `setup_agent()` so every session follows the
  same conventions
- **Sandboxed code execution** — the agent writes and runs Python in a
  managed container you never provision
- **Custom tools** — the agent in the cloud calls functions on your laptop
  over the event stream; swap the mock JSON for a Datadog client and it's
  production
- **Stateful sessions** — the dropdown above the chat lists every past
  session via `sessions.list()`; pick one and the conversation reloads from
  `events.list()`. No database, no local state.

## Repo layout

```
agent.py            ← the only file you edit
agent_complete.py   ← reference implementation
provided.py         ← system prompt, tool schemas, chat UI, session picker
e2e.py              ← headless test of the full path

app.py              ← incident overview
pages/              ← Metrics, Logs, Deploys
incident-triage-runbook/  ← the team's runbook skill (SKILL.md)
data/               ← log + metrics + deploys + diff fixtures
ui.py, assets/      ← styling
```

## Prerequisites

- Access to the [Claude Console](https://platform.claude.com/dashboard)
- An `ANTHROPIC_API_KEY`, created in the Console
- Python 3.10 or above

## Resources

- [Slide deck](https://claude.ai/artifact/5d5nWTK4wWUzowLkvwm9N3)
- Animation of the incident investigation: [play it here](https://htmlpreview.github.io/?https://github.com/sujee/anthropic-cwc-workshops/blob/main/ship-your-first-managed-agent/my/incident-replay.html) · [online copy](https://claude.ai/artifact/MnkY9JX5ukWHjcpqdmnY2Q) · [source file](my/incident-replay.html)
- Managed Agents docs: [overview](https://platform.claude.com/docs/en/managed-agents/overview) · [quickstart](https://platform.claude.com/docs/en/managed-agents/quickstart) · [environments](https://platform.claude.com/docs/en/managed-agents/environments)

## License

MIT

---

**Next → [Lab notes](my/lab-notes.md)**
