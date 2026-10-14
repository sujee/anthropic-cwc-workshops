# 01 · Getting started

[Back to README](README.md) · Next: [02 · Inspect the environment](02-inspect-environment.md)

**Why.** I wanted to run the workshop example end to end myself, and see where the learning experience could be better.

## Past delivery

I watched an earlier delivery of this workshop: https://www.youtube.com/watch?v=19HDQ9HppOA

Observations:

- need more talking points
- architecture diagrams
- more diagrams would help to explain the behavior

(The [slide deck](07-slides.md) and the [animation](05-animation.md) try to address these.)

## Setup

```bash
git clone https://github.com/sujee/anthropic-cwc-workshops/

cd ship-your-first-managed-agent
cp .env.example .env
# set ANTHROPIC_API_KEY in .env

python -m venv .venv
source .venv/bin/activate
pip install -r requirements.txt
```


Then I asked Claude:

```
verify my API key from .env works.
```

## Run

```bash
python data/generate_log.py

streamlit run app.py
```

## Code update

Used [agent_complete.py](../agent_complete.py) to get it working!

## Prompt

From the Streamlit UI I pasted an error text about p99 and asked the agent to solve it.

## Verification

Logged into the [dashboard](https://platform.claude.com/workspaces/default/environments) to see all the artifacts the run created.

## A small fix: the model name was hard-coded

The model name was repeated across files.

Claude prompt:

```
make the model name as a constant to be used throughout.  Let's use claude-sonnet-5-5.
And verify the model works
```

It updated `provided.py` and ran `e2e.py` to verify.

## What I took from this

The example is easy to follow and run, and the use case is realistic. What I wanted more of was the big picture: how the pieces fit together. That is what the rest of this folder is about.

---

[Back to README](README.md) · Next: [02 · Inspect the environment](02-inspect-environment.md)
