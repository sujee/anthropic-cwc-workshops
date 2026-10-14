# Updates

A short timeline of what I did, grouped by topic. The slides, notes and scripts were worked on side by side, so the order is approximate. The detail is on each page. Back to the [README](README.md).

## 2026-10-14

| Step | What | Page |
|---|---|---|
| 1 | Made the model name a constant (`claude-sonnet-5-5`) and checked it with `e2e.py` | [01](01-getting-started.md) |
| 2 | Wrote [managed-env.py](managed-env.py) to look inside a managed environment | [02](02-inspect-environment.md) |
| 3 | Wrote [env-kill.py](env-kill.py): delete the environment mid-session | [03](03-kill-experiments.md) |
| 4 | Wrote [deployment-kill.py](deployment-kill.py): archive a deployment mid-run | [03](03-kill-experiments.md) |
| 5 | Wrote [sandbox-kill.py](sandbox-kill.py): kill the sandbox from inside. The control worked, the kill never ran, and a wrong verdict in my script was fixed. | [03](03-kill-experiments.md), [08](08-lessons.md) |
| 6 | Wrote [list-resources.py](list-resources.py) and [cleanup.py](cleanup.py), and removed 18 leftover resources | [04](04-resources.md) |
| 7 | Added slide sections: Understanding managed agents, Experiments, Best practices | [07](07-slides.md) |
| 8 | Recorded a real run with [capture-events.py](capture-events.py) and built the [animation](incident-replay.html) | [05](05-animation.md) |
| 9 | Wrote the personal tutor | [06](06-tutor.md) |
| 10 | Moved all scripts into this folder and fixed `capture-events.py`, which needed its paths updated | [08](08-lessons.md) |
| 11 | Split these notes into numbered pages | this page |

## Still open

- Does a killed sandbox start a new one on its own? (not yet tested: the kill never ran)
- What does `--kill pause` do to a deployment?
- Does `deployment.status` ever change after an archive?

---

[Back to README](README.md)
