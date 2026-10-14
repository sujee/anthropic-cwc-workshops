# 03 · Kill experiments

[Back to README](README.md) · Previous: [02 · Inspect the environment](02-inspect-environment.md) · Next: [04 · Resources](04-resources.md)

**Why.** My real question was: *if the sandbox gets terminated, will a new one start automatically?* I tried to answer it by removing things from under a running session, one level at a time.

All results below come from **single runs** unless noted. Treat them as observations, not guarantees.

| # | Experiment | Script | What we saw | Confidence |
|---|---|---|---|---|
| 1 | Delete the environment mid-session | [env-kill.py](env-kill.py) | The running command finished. The next message ended the session. | Cause **not proven** |
| 2 | Archive the deployment mid-run | [deployment-kill.py](deployment-kill.py) | The running session finished. No new runs. Manual run and update rejected. | One run |
| 3 | Kill the sandbox from inside | [sandbox-kill.py](sandbox-kill.py) | The kill never ran. | **Inconclusive** |

The slides cover the same ground, with timelines: see the Experiments section in [07 · Slides](07-slides.md).

## 1 · Delete the environment mid-session

**The prompt I gave Claude**

```
i want to explore what happens when the env is destroyed during the middle of session.
Write me code to explore this.
```

**What the script does.** Starts a session on a bash loop, deletes the environment `--kill-after` seconds in, logs every event with a timestamp, then sends a follow-up message that needs a sandbox.

```bash
python my/env-kill.py --kill-after 10
```

**Result (a 20-second task)**

| Time | Event |
|---|---|
| 3.6s | The agent starts the bash loop |
| 7.4s | The environment delete returns OK |
| 24.3s | The tool result arrives with all 10 ticks |
| 25.6s | The session goes idle |
| 26.6s | The follow-up message produces `session.error`, then `session.status_terminated` |

- The delete succeeded although a session was using the environment. The docs say an environment can only be deleted when no sessions reference it.
- The session status read `idle` afterward, so nothing hinted that its environment was gone.
- **Not proven:** that the delete caused the termination. I did not log the error details, and I did not run a control without the delete.

## 2 · Archive the deployment mid-run

**The prompt**

```
We want to terminate deployment.. and see what happens.
write a program to experiment
```

**What the script does.** Creates a deployment that fires every minute. When the first fire starts a session, it archives the deployment 20 seconds later, then watches for about 4 minutes and tries a manual run and an update.

```bash
python my/deployment-kill.py --kill archive
```

**Result**

| Time | Event |
|---|---|
| 45.3s | The first scheduled fire starts a session |
| 65.8s | `deployments.archive` returns OK |
| 173.4s | The session goes idle, after its full 2-minute command |
| 173s to 312s | No new runs, although two more fires were due |
| 311.8s | A manual run and an update both return `400 Cannot modify archived deployment` |

- Archive stops the schedule but does not touch a session that is already running.
- **Surprise:** `deployment.status` still read `active` after the archive. Do not use it to detect an archive.
- **Not tested:** `--kill pause`, a longer wait, a control run.

## 3 · Kill the sandbox from inside

**The question**

```
if the sandbox gets terminated.. will it be started automatically?
```

**What the script does.** Turn 1 writes a marker file and records a fingerprint (hostname, PID 1 start time, uptime). Turn 2 kills the sandbox from inside while the environment stays. Turn 3 looks for the marker. A missing marker with working commands would mean a new sandbox started on its own.

```bash
python my/sandbox-kill.py --method none      # control
python my/sandbox-kill.py --method killall   # kill -9 -1
```

**Result**

- **Control (`--method none`):** worked as designed. The marker was still there, PID 1 had the same start time, and uptime grew by the elapsed time.
- **`--method killall`, two runs:** **inconclusive.** The model returned an empty reply and never ran the kill, even with a system prompt saying the sandbox was disposable and every command authorized. With no kill, turn 3 never ran its check either.
- My first version of this script printed "no automatic restart observed" for those runs. That was a bug in its verdict logic, not a finding. See [08 · Lessons](08-lessons.md).

## Where this leaves the question

**Still open:** does a killed sandbox restart on its own? Neither the environment delete nor the deployment archive killed a sandbox, and the direct kill was never run.

What the experiments did show is a pattern: removing a parent resource did not stop work already in flight, but it blocked what came next.

**Ideas for next time**
- Try `--method init` (`kill -9 1`), though I expect the same empty reply.
- Find a way to end the sandbox that does not depend on the model.
- Run a control for experiment 1, and log the full `session.error` payload.
- Test `--kill pause` for the deployment.

## Next

These runs leave resources behind. [04 · Resources](04-resources.md) is how I found and removed them.

---

[Back to README](README.md) · Previous: [02 · Inspect the environment](02-inspect-environment.md) · Next: [04 · Resources](04-resources.md)
