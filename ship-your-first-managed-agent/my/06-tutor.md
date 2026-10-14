# 06 · My Tutor: Incident-2277 and Managed Agents

[Back to README](README.md) · Previous: [05 · Animation](05-animation.md) · Next: [07 · Slides](07-slides.md)

**Why.** Learning has a new paradigm.

For years, learning meant finding the docs, reading them, watching long videos, trying the code, getting stuck and searching for answers. 

Now I start with an agent. It reads the code and the docs with me, explains at my level, quizzes me, and runs an experiment the moment I get curious. The agent does the legwork and I do the thinking. I call this **agent-first learning**, or *agent-assisted learning*.

| | The old way | Agent-first |
|---|---|---|
| Where I start | read the docs, watch a long video | ask the agent |
| The explanation | one level for everyone | at my level, in my words |
| Checking myself | at the end, if at all | all the time, because the agent quizzes me |
| A curious moment | write it down, look it up later | run the experiment now |

This page is that idea applied to one example: a personal tutor for `ship-your-first-managed-agent`. It **explains** the example and **quizzes** me on it.

## How to use this file

1. Open Claude Code in this directory (`ship-your-first-managed-agent/`).
2. Paste this, then pick a mode from the menu it offers:

```text
Read my/06-tutor.md, then act as my tutor using the "Tutor brief" section.
If my/progress.md exists, read it first and pick up from there.
Start by asking which mode I want and how much time I have.
```

3. The tutor keeps score in `my/progress.md` (it creates the file). Ask it to "show my progress" any time.

---

## 1. Tutor brief (the rules the tutor follows)

```text
You are my tutor for the Incident-2277 example (Claude Managed Agents).
Ground everything in the real files in this repo: agent.py, agent_complete.py,
provided.py, e2e.py, data/, incident-triage-runbook/SKILL.md, and my own
experiments in my/ and the *-kill.py scripts.

Rules
- One question at a time. Wait for my answer before revealing anything.
- Never give the answer before I have tried. Use a hint ladder:
  hint 1 = where to look, hint 2 = the concept, hint 3 = the answer.
- After I answer: say what is right, what is missing, then give the answer.
- Quote the file and function when you explain. Do not describe code from memory.
- Never invent API behaviour. If you are not sure, say so, then read the docs
  (platform.claude.com/docs/en/managed-agents) or run a small experiment.
  Tell me which of my results were seen only once (see section 7).
- Keep each explanation under 10 lines unless I ask for more. Use a diagram
  (ASCII is fine) when a mechanism is easier to see than to say.
- Mix difficulty: start easy, step up after two right answers in a row,
  step down after two misses.
- Track results in my/progress.md: topic, question, right/wrong, date.
  Bring back anything I missed after 1 day, 3 days and 7 days.
- Offer a hands-on exercise from section 5 when I get bored of questions.
  Tell me what it will cost in API credits before I run it.
```

---

## 2. The example on one page (cheat sheet)

**The story.** 2am page: checkout p99 latency is 10x baseline. Cause: commit `a3f9c21`, deployed 14:31:18 UTC, replaced one batched query with a per-order loop (an N+1). p99 went from about 65 ms to about 3,600 ms, the DB pool filled, and about 20% of checkouts failed. The agent has to find this across four sources.

**The four resources**

| Resource | What it is | Created by |
|---|---|---|
| Agent | model + prompt + tools + skills. Stored settings. Runs nothing. | `setup_agent()` |
| Environment | the sandbox settings (networking, packages). Stored settings. | `setup_environment()` |
| Session | one conversation. The only thing that runs. Gets its own fresh sandbox. | `start_session()` |
| Events | messages in both directions on the stream | `stream_reply()` |

**The seven functions in `agent.py`**

| # | Function | API call | Runs where |
|---|---|---|---|
| 1 | `setup_agent()` | `skills.create` + `agents.create` | Anthropic stores it |
| 2 | `setup_environment()` | `environments.create` | Anthropic stores it |
| 3 | `upload_log()` | `files.upload` | Anthropic stores it |
| 4 | `start_session()` | `sessions.create` | Anthropic runs it |
| 5 | `stream_reply()` | `events.stream` + `events.send` | **my machine** |
| 6 | `handle_tool()` | none, reads `data/*.json` | **my machine** |
| 7 | `delete_session()` | `sessions.delete` | Anthropic |

**Who runs what.** Bash and grep run in the agent's sandbox. `get_metrics`, `get_recent_deploys` and `get_diff` are custom tools: the agent asks, **your** `handle_tool()` answers.

**The event loop in plain words**
```
you   -> user.message
agent -> agent.message / agent.tool_use              (sandbox tools, you only watch)
agent -> agent.custom_tool_use                       (agent now waits for you)
you   -> user.custom_tool_result                     (answer it)
agent -> session.status_idle with stop_reason end_turn   (done)
```

**Data files.** `app.log` (70k JSON lines, searched in the sandbox), `metrics.json`, `deploys.json`, `diff.txt` (served by your tools).

---

## 3. Explain mode: prompts to paste

**Warm-up**
```text
Explain this example in 5 sentences, then ask me to say it back in my own words.
```
```text
Walk me through agent.py one function at a time. After each one, ask me one
question before moving on.
```

**Trace it (my favourite)**
```text
Trace one question, "what caused the latency spike?", from the moment I press
Enter to the final answer. List every event in order with who sends it. Then
blank out three events and make me fill them in.
```

**Change the audience**
```text
Explain Managed Agents three times: to a 12-year-old, to a backend engineer,
and to a CTO who thinks "we can just call the Messages API in a loop".
```

**Why is it designed this way?**
```text
Pick one design decision (sandbox for the log, custom tools for private data,
skill for the runbook, server-side sessions). Argue the opposite design.
Make me defend the original.
```

**Draw it**
```text
Draw the architecture as an ASCII diagram. Mark what runs on my laptop and
what runs on Anthropic's side. Then redraw it for a deployment that fires every Friday.
```

**Read the code with me**
```text
Open provided.py. Explain _load_history() and chat_panel() the way a code
reviewer would. What would I change before using this in production?
```

---

## 4. Quiz mode: formats and prompts

| Format | Prompt to paste |
|---|---|
| Flashcards | `Give me 10 flashcards on the four resources. Show the front, wait, then the back.` |
| Multiple choice | `5 multiple-choice questions, 4 options each, with plausible wrong answers taken from real misconceptions.` |
| Predict the output | `Show me a code snippet from this repo and ask what it prints or does. Do not run it until I answer.` |
| Fill the blank | `Take a function from agent_complete.py, remove 3 lines, and ask me to write them back.` |
| Next event? | `Describe a point in the event stream and ask what event comes next.` |
| Spot the bug | `Plant one bug in a copy of agent.py (do not tell me which). I find it, then we run it to verify.` |
| True or false trap | `10 statements that sound true but are subtly wrong. I say which and why.` |
| Whiteboard | `Ask me to draw the architecture from memory in ASCII, then grade it against the real one.` |
| Pre-mortem | `Ask me for 5 ways this agent fails in production. Grade my list and add the ones I missed.` |
| Boss fight | `20 questions mixed from every topic. No hints. Score me at the end.` |

### Bugs for "spot the bug" (tutor picks one in secret)
Predict the failure first, then verify by running or reading the docs. These are plausible bugs, so check each before trusting it.

1. Hard-coded skill `display_name`, so a second run fails (the comment in `agent.py` explains this).
2. `@st.cache_resource` removed from `setup_agent()`, so every Streamlit rerun creates another agent.
3. `events.send(...)` called before the stream is opened, so early events can be missed.
4. `stream_reply()` never sends `user.custom_tool_result`, so the agent waits on a tool answer.
5. The loop breaks on any `session.status_idle`, not only `stop_reason.type == "end_turn"`. Look at how `provided.py` checks it.
6. `handle_tool()` returns a dict, not a string, in the result content.
7. Wrong id used for `custom_tool_use_id` in the result.
8. `networking` left `unrestricted` in something meant for production.

---

## 5. Hands-on exercises (a ladder)

Costs: A means free to do or tiny, B means a few API calls, C means a longer session or scheduled resources. Always run `python my/cleanup.py` afterwards (dry run first).

| # | Exercise | What you learn | Cost |
|---|---|---|---|
| 1 | **Predict, then run `e2e.py`.** Write down the tool order you expect, then compare. | the loop and the runbook order | B |
| 2 | **Event safari.** Log every `event.type` you see and group them into "mine", "agent's" and "bookkeeping". | the event stream | B |
| 3 | **Muzzle the agent.** Remove the `get_diff` tool. Predict the conclusion, then run. | what each tool contributes | B |
| 4 | **Poison the runbook.** Edit `SKILL.md` to say "grep the log first". Compare the tool order. | skills shape process | B |
| 5 | **Decoy deploy.** Add an innocent deploy a minute before the bad one to `deploys.json`. Does the agent get fooled? | correlation and diffs | B |
| 6 | **A new outage.** Write a different cause (missing index, removed cache decorator) in a new `diff.txt` and log. Can it find it? | does the runbook generalise | B |
| 7 | **Cost detective.** Print `session.usage` per turn and total it. Where do the tokens go? | cost and compaction | B |
| 8 | **Add a fourth tool.** `get_oncall()`: schema in `provided.py`, handler in `handle_tool()`. | the custom tool contract | B |
| 9 | **Lock it down.** Switch to `limited` networking. What breaks, and what do you add to `allowed_hosts`? | least privilege | B |
| 10 | **Marker file.** Two sessions on one environment. Write a file in one, look for it in the other. | sandbox isolation | B |
| 11 | **Break glass.** Predict, then run `env-kill.py`, `deployment-kill.py`, `sandbox-kill.py --method none`. | what survives a kill | B/C |
| 12 | **Schedule it.** Draft `deployments.create(...)` that triages every weekday 9am. Do not run it until you can say how to stop it. | deployments, pause vs archive | C |

---

## 6. Creative formats (pick one when bored)

- **Incident Commander.** Tutor plays PagerDuty and tells me what is on fire. I ask the agent, then brief the tutor.
- **Teach-back.** I teach the tutor, who plays a confused junior engineer and asks naive questions.
- **Mutation testing.** Tutor secretly breaks one line in a scratch copy. I have 5 minutes.
- **Squeeze.** Explain the example in 5 sentences, then 1 sentence, then a tweet.
- **Docs scavenger hunt.** "Find where the docs say X." I get 3 minutes and a point per correct link.
- **Event stream bingo.** Tutor reads a real event log with the types hidden. I name each one.
- **Rubber duck.** I explain a failure to the tutor. The tutor may only ask questions.
- **Spot the lie.** Tutor gives 5 sentences about managed agents, one false. Which?

---

## 7. Common misconceptions (and what my experiments showed)

Experiments marked **(once)** were single runs. Treat them as observations, not guarantees.

| Misconception | Reality |
|---|---|
| "The environment is a running container." | It is a stored setting. Each session builds its own fresh sandbox from it. |
| "A deployment runs the agent." | A deployment stores a schedule and creates sessions. The session runs. |
| "Archive and delete are the same." | Archive of a deployment is final. Pause is reversible. |
| "Deleting the environment kills a running session." | The running command finished in my run. **(once)** The next message ended the session. **(once)** The cause is not proven. |
| "Archiving a deployment stops its running session." | The session finished normally. **(once)** Future fires stopped. **(once)** |
| "`deployment.status` shows archived after archive." | It still read `active` for the rest of the run. **(once)** |
| "Sandboxes restart when killed." | **Unanswered.** The kill never ran: the model returned an empty reply. |
| "The log goes into the model's context." | It stays in the sandbox. Only grep results come back. |
| "The agent runs my tools." | It asks. Your `handle_tool()` answers over the event stream. |

---

## 8. Spaced review plan

| When | What |
|---|---|
| Day 0 | Sections 2 and 3, then 10 flashcards |
| Day 1 | Re-ask everything I missed. Trace one question from memory. |
| Day 3 | Spot the bug (pick 2). Exercise 1 or 3. |
| Day 7 | Boss fight, then one creative format |
| Day 14 | Teach-back to someone else, or do a slide for the deck |

## 9. Progress tracker (the tutor updates `my/progress.md`)

- [ ] I can name the four resources and say which ones run
- [ ] I can trace one question event by event
- [ ] I can say who runs `handle_tool()` and why
- [ ] I can explain why the log is not pasted into the prompt
- [ ] I can explain skill vs system prompt
- [ ] I can name three ways a session fails and what I see
- [ ] I can explain a deployment and what pause and archive do
- [ ] I can design the sandbox-kill test from memory

---

## 10. Answer key (the tutor holds this back)

<details>
<summary>Open only after trying</summary>

1. **Why upload `app.log` instead of pasting it?** About 15 MB, roughly 7.5M tokens, against a 1M-token window. In the sandbox, grep reads it in place and only matches come back.
2. **Who runs `handle_tool()`?** My machine. The agent emits `agent.custom_tool_use`, my loop answers with `user.custom_tool_result`.
3. **What if I never send the tool result?** The agent waits. The session sits idle without an `end_turn`.
4. **Which event ends a turn?** `session.status_idle` with `stop_reason.type == "end_turn"`.
5. **Why the uuid suffix on the skill name?** `display_name` has to be unique per organization.
6. **What does `@st.cache_resource` do here?** Runs the setup once per Streamlit process, so the agent, environment and upload are not re-created on every rerun.
7. **Where is the conversation stored?** On Anthropic's side. `sessions.list()` and `events.list()` rebuild it, so no local database is needed.
8. **Skill vs system prompt?** The prompt is always in context and holds generic facts. The skill holds the team's process and is opened when the task matches its description.
9. **Do sessions on one environment share files?** No. Each gets its own fresh sandbox.
10. **Root cause?** `a3f9c21`: a batched query became a per-order query in a loop (N+1).
11. **Order of evidence?** Deploy at 14:31:18, p99 moves a minute or two later, the DB pool is full around 14:37, errors begin around 14:40.
12. **Why does the runbook say deploys first, log last?** To correlate before searching, so the agent confirms a hypothesis instead of fishing in 70k lines.
13. **Biggest risk in this repo's environment?** `networking: unrestricted`. Use `limited` with `allowed_hosts` for real data.
14. **Open the stream before or after sending the message?** Before. The quickstart sends after the stream opens.
15. **Deployment fires but its environment is archived?** The run records an error (for example `environment_archived_error`) and the deployment pauses itself (from the docs, not tested here).

</details>

---

[Back to README](README.md) · Previous: [05 · Animation](05-animation.md) · Next: [07 · Slides](07-slides.md)
