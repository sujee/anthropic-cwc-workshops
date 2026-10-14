# My Exploration and Updates

**TLDR;**

> Very good example.  I was able to follow and run this example pretty easily.  
> So focused on **improving learning experience**  
> Also wanted to make this **agent-assisted learning**  


**What I did.** With an agent beside me, I ran the workshop example and wanted a clearer big picture. I looked inside a managed environment, tried to break things to learn what survives, tracked the resources my tests left behind, and turned what I learned into slides, an animation and a tutor.

## ⭐️ Deliverables

- ⭐ **My favourite: a personal AI tutor** that walks me through this example and quizzes me. Try it: [06-tutor.md](06-tutor.md)
- [new slide deck i created](https://claude.ai/artifact/5d5nWTK4wWUzowLkvwm9N3#slide-881107b50de7)
- A cool animation showing what's happening: [play it here](https://htmlpreview.github.io/?https://github.com/sujee/anthropic-cwc-workshops/blob/main/ship-your-first-managed-agent/my/incident-replay.html) · [online copy](https://claude.ai/artifact/MnkY9JX5ukWHjcpqdmnY2Q) · [source file](incident-replay.html)

## The pages

Read them top to bottom. Each page links to the next.

| # | Page | What it covers | Scripts |
|---|---|---|---|
| 01 | [Getting started](01-getting-started.md) | Setup, running the example, past delivery notes, the model-name fix | |
| 02 | [Inspect the environment](02-inspect-environment.md) | What is inside a managed environment | [managed-env.py](managed-env.py) |
| 03 | [Kill experiments](03-kill-experiments.md) | Delete the environment, archive the deployment, kill the sandbox. One result is inconclusive. | [env-kill.py](env-kill.py), [deployment-kill.py](deployment-kill.py), [sandbox-kill.py](sandbox-kill.py) |
| 04 | [Resources](04-resources.md) | List everything in the account, and clean up what tests left | [list-resources.py](list-resources.py), [cleanup.py](cleanup.py) |
| 05 | [Animation](05-animation.md) | A replay of one real agent run | [capture-events.py](capture-events.py), [incident-replay.html](incident-replay.html) |
| 06 | ⭐ [Tutor](06-tutor.md) | **Start here to learn the example.** Explain and quiz modes, exercises, games | |
| 07 | [Slides](07-slides.md) | The deck, and the sections I added | |
| 08 | [Lessons](08-lessons.md) | What worked, and what fooled me | |

[updates.md](updates.md) is the short timeline of all of the above.

## My Conclusion

what i liked:
- use case is 'realistic' but simple enough to accomplish
- setup was easy
- following through instructions was straight forward
- code wasn't overly complicated.

what I wanted to see more of:
- 'big picture' of how it all came together
- I like more diagrams / workflows than text
- use cases for managed agents
- little exploration of concepts 

## Running the scripts

Run them from the project folder, with the project's virtual environment active:

```bash
source .venv/bin/activate
python my/list-resources.py
```

## References

- doc : https://platform.claude.com/docs/en/managed-agents/quickstart
- past delivery: https://www.youtube.com/watch?v=19HDQ9HppOA
