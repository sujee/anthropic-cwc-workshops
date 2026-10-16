# Lab Notes - 4 - Your Personal AI Tutor

[← Lab notes](lab-notes.md) · Previous: [3 - Bonus Materials](lab-notes-3.md)

In this lab, you will use Claude Code as a personal tutor for this workshop. It **explains** the example at your level and **quizzes** you on it.

The tutor's rules, cheat sheet, quizzes and exercises are all in [06 · Tutor](06-tutor.md). You don't need to read it first: the tutor reads it for you.

## 1 - Start the tutor

1 - Start Claude Code in the `ship-your-first-managed-agent` folder

```bash
claude
```

2 - Paste this prompt

```text
Read my/06-tutor.md, then act as my tutor using the "Tutor brief" section.
If my/progress.md exists, read it first and pick up from there.
Start by asking which mode I want and how much time I have.
```

3 - Pick a mode from the menu it offers

## 2 - Pick a mode

| Mode | What it does | Try this |
|---|---|---|
| **Explain** | Walks you through the code and concepts | `Walk me through agent.py one function at a time. After each one, ask me one question before moving on.` |
| **Trace** | Follows one question event by event | `Trace "what caused the latency spike?" from the moment I press Enter to the final answer. Then blank out three events and make me fill them in.` |
| **Quiz** | Flashcards, multiple choice, spot the bug and more | `Give me 10 flashcards on the four resources. Show the front, wait, then the back.` |
| **Hands-on** | Small experiments on the real code | `Pick an exercise from section 5 for me. Tell me what it costs before I run it.` |
| **Boss fight** | Mixed questions from every topic, no hints | `20 questions mixed from every topic. No hints. Score me at the end.` |

More prompts are in [06 · Tutor](06-tutor.md), sections 3 to 6.

## 3 - How the tutor works

- It asks **one question at a time** and waits for your answer.
- It never gives the answer first. It uses a hint ladder: where to look, then the concept, then the answer.
- It quotes the real files in this repo instead of describing code from memory.
- It keeps score in `my/progress.md` (git-ignored). Ask it to **"show my progress"** any time.
- It brings back questions you missed after 1, 3 and 7 days.

**Explore**

- Ask it something you're unsure about from labs 1–3, like *"does a killed sandbox restart?"*. Does it tell you what's proven and what's still open?
- Try **Teach-back**: you teach the tutor, and it plays a confused junior engineer.
- Before a hands-on exercise, ask what it will cost in API credits.

> Hands-on exercises create resources. Run `python my/cleanup.py` afterwards (dry run first), as in [lab 3](lab-notes-3.md#2---resource-management---cleanup-scripts).

---

[← Back to lab notes](lab-notes.md)
