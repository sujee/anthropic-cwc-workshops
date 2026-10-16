# Lab Notes - Part 2 - Building an SRE Agent

[← Lab notes](lab-notes.md) · Previous: [Part 1](lab-notes-1.md)

In this lab, we will build an SRE managed agent.

## 1 - Setup

Be sure you have completed the [setup](lab-notes-1.md#2---setup) from Part 1.

## 2 - Create logs

Create the incident logs used in this exercise.

### Run this script

```bash
python data/generate_log.py
# writes data/app.log (70k lines, not in git)
```

Open `data/app.log` and inspect the data.

## 3 - Launch the Streamlit app

This will serve as our dashboard.

```bash
streamlit run app.py
```

This opens the UI in your browser: http://localhost:8501/

### Inspect the UI

Click through the **Metrics**, **Logs** and **Deploys** pages. Notice the **SRE Agent** chat panel on the side: it's offline for now.

## 4 - Build out the SRE Agent

Time: ~20 min

The agent code is in [agent.py](../agent.py). It has stubs for the functions we need to fill in.

The complete agent is in [agent_complete.py](../agent_complete.py).

In the interest of time, we will copy from **agent_complete.py** to fill in the stubs in **agent.py**.

> **Bonus lab:** once you are comfortable with the Managed Agents API, try writing the stubs on your own.

Fill in the stubs in this order. After each one, watch the app change live!

1. `setup_agent`
2. `setup_environment`
3. `upload_log`
4. `start_session`
5. `stream_reply`
6. `handle_tool`
7. `delete_session`

## 5 - Inspect the Console

- Log in to the [Claude Console](https://platform.claude.com/workspaces/default/environments)
- Inspect **Agents** and **Sessions**
- You will see our newly created SRE agent, alive!

## 6 - Run the agent

In the UI, **create a new session**.

Ask the agent:

```text
investigate this issue
checkout.p99_latency_ms > 500 for 5m
```

Watch the agent:

- investigate using the [skill](../incident-triage-runbook/SKILL.md)
- make custom tool calls back to our app
- diagnose the issue and suggest a fix!

Pretty cool, eh!

## 7 - Understand the SRE Agent workflow

First, let's look at this animation:
[play it here](https://htmlpreview.github.io/?https://github.com/sujee/anthropic-cwc-workshops/blob/main/ship-your-first-managed-agent/my/incident-replay.html) · [online copy](https://claude.ai/artifact/MnkY9JX5ukWHjcpqdmnY2Q) · [source file](incident-replay.html)

Now let's quickly look through the [slides](https://claude.ai/artifact/5d5nWTK4wWUzowLkvwm9N3) to understand the concepts.

## 8 - Done 👏

We built a working SRE agent on Managed Agents, running in a managed environment.

---

**Next → [Part 3 - Bonus Materials](lab-notes-3.md)**

[← Back to lab notes](lab-notes.md)
