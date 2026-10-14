# 08 · Lessons from working with Claude

[Back to README](README.md) · Previous: [07 · Slides](07-slides.md)

I called this *agent-assisted learning*. These are the things that worked, and the things that went wrong, while Claude and I did it.

## When a result can fool you

**1. A script's verdict is only as good as its definition of failure.** My first `sandbox-kill.py` printed "no automatic restart observed". The real story was that the agent never ran the kill, so nothing was tested. The script treated "the agent ran nothing" as "the sandbox is dead". The fix was a third outcome, INCONCLUSIVE, and a check that the command actually ran. See [03](03-kill-experiments.md).

**2. Run a control first.** The control run of `sandbox-kill.py` proved the marker-file check worked before I trusted any other verdict. `env-kill.py` had no control, and its conclusion is still unproven.

**3. One run is an observation.** I marked single-run results as such, in the notes and on the slides. That kept me from over-claiming.

**4. Check the docs against what happens.** Two surprises, both from single runs: an environment delete succeeded while a session was using it (the docs say it can't), and `deployment.status` still read `active` after an archive.

## When a page can fool you

**5. Look at the thing you built.** The animation page showed an empty narration, empty meters and no answer. The log looked fine, so a quick glance would have passed it. A script error part-way through the first render caused it, and a screenshot made it obvious. See [05](05-animation.md).

**6. Real data beats a mock-up.** I recorded a real run and replayed it, instead of inventing events. Every event on screen is one that actually happened.

## Habits that paid off

**7. Name what you create, and list it.** Every experiment left an environment and an agent behind. A shared name prefix, a list script and a dry run made cleanup safe. See [04](04-resources.md).

**8. Say what to build, not how.** The prompt that produced the animation got shorter and better when I described the result and left out the implementation. See [05](05-animation.md).

**9. Moving files breaks hidden paths.** When I moved the scripts into this folder, six worked unchanged and one (`capture-events.py`) needed edits, because it found its neighbours by relative path. Test after a move.

**10. Ask for the open question.** The most useful moment was writing down what is still not answered: whether a killed sandbox restarts. A clear "not shown yet" is worth more than a confident wrong answer.

## What I would do differently

- Write the control for each experiment first.
- Log full error payloads from the start.
- Review the rendered slides and page by eye before calling them done.

---

[Back to README](README.md) · Previous: [07 · Slides](07-slides.md)
