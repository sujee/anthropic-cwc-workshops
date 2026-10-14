# 05 · Animation: replay of an SRE agent run

[Back to README](README.md) · Previous: [04 · Resources](04-resources.md) · Next: [06 · Tutor](06-tutor.md)

**Why.** The earlier delivery needed more diagrams. A replay of a real run shows the event stream in motion, which is hard to see in static slides.

An animated replay of one real run of the SRE agent. It shows each event travelling between my machine and Anthropic's cloud, with an event log that highlights the current event.

- **Play it on GitHub:** [open the animation](https://htmlpreview.github.io/?https://github.com/sujee/anthropic-cwc-workshops/blob/main/ship-your-first-managed-agent/my/incident-replay.html). GitHub shows `.html` files as source, so this link uses a free viewer that renders the page.
- **The source file:** [incident-replay.html](incident-replay.html). On GitHub this shows the code. Download it and open it in a browser to play it.
- **Online copy:** https://claude.ai/artifact/MnkY9JX5ukWHjcpqdmnY2Q
- **The recorded run it plays:** [run-events.json](run-events.json)
- **Script that recorded the run:** [capture-events.py](capture-events.py)

## The prompt

```text
Build an animated replay of one real run of the SRE agent in this example.

Record a real run first, then make a single self-contained HTML page that plays it back:
- a diagram of my machine vs Anthropic's cloud, with each event travelling between them
- an event log that highlights the current event
- play/pause, speed, and a scrubber
- token counts, and the agent's final answer when it arrives

Open it showing the finished run, with a button to replay it. Save it in my/.
```

## Local file vs the online copy

The two are the same animation, but the files differ in one way. The online page is wrapped in a standard document skeleton when it is published. That skeleton includes a rule that makes the `hidden` attribute actually hide things. The first local copy did not have it, so the event log never cleared when the replay started, and the page ran in quirks mode.

`incident-replay.html` in this folder is now a complete page with that skeleton included, so it behaves the same as the online copy. If you ever republish it to the artifact, publish the bare page (without the `<!doctype>` and `<html>` wrapper), because the platform adds the wrapper itself.

---

[Back to README](README.md) · Previous: [04 · Resources](04-resources.md) · Next: [06 · Tutor](06-tutor.md)
