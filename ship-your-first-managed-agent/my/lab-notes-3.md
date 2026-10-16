# Lab 3 — Bonus Materials

[← Lab notes](lab-notes.md) · Previous: [2 - Building an SRE Agent](lab-notes-2.md)

Here are some bonus activities for you to explore. There are no right answers here. For each one: **predict** what will happen, **run** it, then **compare** with what you saw.

Run all commands from the `ship-your-first-managed-agent` folder.

## 1 - Take an inventory

See what is in your account.

```bash
python my/list-resources.py
```

It prints every agent, environment, session and deployment as a tree. It is read-only.

**Explore**

- How many agents and environments do you have? More than you expected?
- Which environments have no sessions? Where did they come from?
- Every run of `my/managed-env.py` in lab 1 creates an `env-inspect-*` environment and an `env-inspector-*` agent. Can you spot yours?
- Is there a session whose environment shows as `(deleted)`?

## 2 - Resource Management - Cleanup scripts

Now clean up. The script only touches resources whose names start with the test-script prefixes (`env-kill-`, `dep-kill-`, `sbx-kill-`, `env-inspect-`, `env-inspector-`). The workshop's own `SRE Agent` resources are never touched.

```bash
python my/cleanup.py          # dry run: list what would be removed
python my/cleanup.py --yes    # remove it
```

Always do the dry run first.

**Explore**

- The script removes things in a fixed order: deployments, then sessions, then environments, then agents. Why does the order matter?
- Some resources are **deleted** and some are only **archived**. Which are which?
- Run `list-resources.py` again. Is everything gone? How would you tell "archived" from "gone"?

My before-and-after run is in [04 · Resources](04-resources.md).

> **A habit worth keeping:** run `python my/list-resources.py` before and after a batch of experiments.

## 3 - Understanding Lifecycle

My question was: *if the sandbox gets terminated, will a new one start automatically?* These scripts remove things from under a running session, one level at a time.

Each script logs every event with a timestamp. Read the timeline, not just the last line.

### 3.1 - Delete the environment mid-session

```bash
python my/env-kill.py --kill-after 10 --ticks 10
```

The script starts a 20-second bash loop (10 ticks of 2s each) in a session, deletes the environment 10 seconds in, then sends a follow-up message that needs a sandbox.

**Predict first:** will the delete be allowed while a session is using the environment? Will the running loop finish?

**Explore**

- Does the bash loop finish all its ticks?
- What is the session status right after the delete? Does it hint that anything is wrong?
- What happens to the follow-up message?
- Try different `--kill-after` and `--ticks` values. Does the outcome change?
- Can you prove the delete *caused* what you saw? What control run would you need?

### 3.2 - Archive a deployment mid-run

```bash
python my/deployment-kill.py --kill archive
```

The script creates a deployment that fires every minute, archives it 20 seconds after the first session starts, then watches for about 4 minutes. Let it run.

**Predict first:** does archiving stop a session that is already running?

**Explore**

- Does the running session finish?
- Do any more scheduled runs fire after the archive?
- What does `deployment.status` say after the archive? Can you trust it?
- What happens when you try a manual run or an update?
- Not tried yet: `--kill pause`. How does it differ from archive?

### 3.3 - Kill the sandbox from inside

```bash
python my/sandbox-kill.py --method none      # control
python my/sandbox-kill.py --method killall   # kill -9 -1
```

Turn 1 writes a marker file and records a fingerprint (hostname, PID 1 start time, uptime). Turn 2 asks the agent to kill the sandbox. Turn 3 looks for the marker. A missing marker with working commands would mean a new sandbox started on its own.

**Predict first:** if the sandbox dies, does the session get a fresh one?

**Explore**

- Run the control first. What do the fingerprints look like when nothing is killed?
- In the `killall` run, did the agent actually run the kill? Read its reply carefully.
- If the kill never ran, what does that tell you about who is really in control of the sandbox?
- Can you think of a way to end the sandbox that does not depend on the model?

### Compare notes

My results and timelines are in [03 · Kill experiments](03-kill-experiments.md). Don't peek until you have your own!

**Big-picture questions**

- Across all three experiments, what happens to work that is already in flight when a parent resource is removed? What about the work that comes next?
- The big question is still open: does a killed sandbox restart on its own? Can you answer it?

### Clean up again

Every experiment above leaves an environment and an agent behind. Repeat [step 2](#2---resource-management---cleanup-scripts): inventory, dry run, then `--yes`.

```bash
python my/list-resources.py
python my/cleanup.py
python my/cleanup.py --yes
```

---

**Next → [4 - Your Personal AI Tutor](lab-notes-4.md)**

[← Back to lab notes](lab-notes.md)
