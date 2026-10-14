# 07 · The slide deck

[Back to README](README.md) · Previous: [06 · Tutor](06-tutor.md) · Next: [08 · Lessons](08-lessons.md)

**Why.** After watching the earlier delivery (see [01](01-getting-started.md)) I wanted the diagrams and the big picture that were missing.

**The deck:** https://claude.ai/artifact/5d5nWTK4wWUzowLkvwm9N3

The deck existed before this work, with sections on what a managed agent is, the use case, the design decisions, the components, the build-along, and failure recovery. Everything below was added on top.

## What I added

| Section | Slides | What it covers |
|---|---|---|
| **Understanding managed agents** | 6 | How agents, environments, sessions and deployments tie together, and which ones actually run. An analogy slide, a "how many of each" diagram, one scheduled fire step by step, and what a deployment depends on. |
| **Best practices** | 6 | Five habits: define once, least privilege, cap the spend, read the event stream right, clean up. Each from the docs or from our own runs. |
| **Experiments** | 6 | The three kill experiments from [03](03-kill-experiments.md) with timelines, plus a "what we know and what we do not" summary. Inconclusive results are marked as such. |

Every slide has a diagram, not just text.

## The requests, in my words

```
add a slide explaining how deployment / environments / session / agents all relate
use diagrams
```

```
add a few slides under 'experiments' section.. 
add your findings with timeline
if the results are not conclusive, say so.. that is fine
```

```
update the slide deck with 'best practices' for using managed agents.
```

I also asked for the slides to be grouped into a section called "understanding managed agents" so they read in order.

## Still to review

I have not looked at how the new slides render, so check these by eye:

- text overflowing a box, or labels overlapping on the diagrams
- the pinned diagrams on the experiments and best-practices slides
- the new section divider slides

## Related

- [05 · Animation](05-animation.md): a replay of one real agent run
- [06 · Tutor](06-tutor.md): explain and quiz modes for this example

---

[Back to README](README.md) · Previous: [06 · Tutor](06-tutor.md) · Next: [08 · Lessons](08-lessons.md)
