# Lab 1 — Understanding Managed Environments

[← Lab notes](lab-notes.md)

In this lab, we will explore Managed Environments.

## 1 - Before you start

- Skim the [slides](https://claude.ai/artifact/5d5nWTK4wWUzowLkvwm9N3#slide-3dd33bdac6c2)
- Log in to the [Claude Console](https://platform.claude.com/workspaces/default/environments)

## 2 - Setup

You need Python **3.10+** and an [Anthropic API key](https://platform.claude.com/settings/keys).

```bash
git clone https://github.com/sujee/anthropic-cwc-workshops/
cd anthropic-cwc-workshops/ship-your-first-managed-agent

python -m venv .venv
source .venv/bin/activate          # Windows: .venv\Scripts\activate

pip install -r requirements.txt
cp .env.example .env

# then put your ANTHROPIC_API_KEY in .env
```

### Verify your API key

1 - Start Claude Code in this dir

```bash
claude
```

2 - And ask it

```text
verify api key in .env works
```

## 3 - Your first managed env (Hello world!)

We will spin up our first managed environment and inspect it.

Code: [managed-env.py](managed-env.py)

### Run it

```bash
python my/managed-env.py
```

### Inspect the output

Sample output:

```json
{
  "os": {
    "name": "Ubuntu",
    "version": "24.04.5 LTS (Noble Numbat)",
    "kernel": "6.18.44-fc-v139",
    "arch": "x86_64"
  },
  "cpu": {
    "model": "Intel(R) Xeon(R) Processor @ 2.10GHz",
    "cores": 4
  },
  "memory": {
    "total": "15Gi",
    "used": "209Mi",
    "free": "15Gi"
  },
  "disks": [
    {
      "filesystem": "/dev/vda",
      "size": "252G",
      "used": "11G",
      "avail": "30G",
      "mount": "/"
    }
  ]
}
```

### Explore the Console

Log in to the [Claude Console](https://platform.claude.com/dashboard) and look at **Environments** and **Agents**.

### Discuss your findings

- The script created an environment, an agent and a session. Which of them can you find in the Console?
- The script deletes the session at the end but keeps the environment. Why reuse an environment instead of creating a new one each time?
- The disk is 252G, with 11G used but only 30G available. What could explain the gap?

Curious what happens when things get removed mid-session? See [03 · Kill experiments](03-kill-experiments.md).

---

**Next → [2 - Building an SRE Agent](lab-notes-2.md)**
