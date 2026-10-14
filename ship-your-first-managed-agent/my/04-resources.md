# 04 · List and clean up resources

[Back to README](README.md) · Previous: [03 · Kill experiments](03-kill-experiments.md) · Next: [05 · Animation](05-animation.md)

**Why.** Every experiment in [03](03-kill-experiments.md) leaves an environment and an agent behind. These two scripts show what is in the account and remove what my tests created.

This page documents what the two scripts do, the output of one run of each, and a summary. Captured 2026-10-14.

| Script | What it does |
|---|---|
| [list-resources.py](list-resources.py) | Prints every agent, environment, session and deployment as a tree. Read-only. |
| [cleanup.py](cleanup.py) | Removes the resources my test scripts created. Dry run unless you pass `--yes`. |

## list-resources.py

**What it does.** Lists everything the account has, with no filters, and prints it as a tree. The nesting follows how the resources are used:

```
agent
└── environment the agent ran in
    ├── session
    └── deployment
```

Environments that no session or deployment uses are printed in their own group at the end. If a session's environment no longer exists, it shows as `(deleted)`. A count line closes the output.

**Run it.**

```bash
python my/list-resources.py
```

### Output before cleanup

```text
agent  agent_01E1tbffo7jX7tAxqhrENrVb  sbx-kill-d683bc  v1  2026-10-14 19:07:57
agent  agent_011FZ2a11rygvv85amk4DPe4  sbx-kill-f8e941  v1  2026-10-14 19:01:31
agent  agent_01WWg2ou5ZJFEWY6VUESUKS3  sbx-kill-826991  v1  2026-10-14 19:00:08
agent  agent_01C3FyJbv9YMVFDVvrgbXH53  dep-kill-b63165  v1  2026-10-14 18:37:17
agent  agent_01RJFVVPxKDSdKoDU1hQTxLA  env-kill-0d77b2  v1  2026-10-14 18:25:30
agent  agent_01Ce781pweUDAiLCx7ZN7mH3  env-kill-5eac6a  v1  2026-10-14 18:21:08
agent  agent_01RzxFioiqmmN9kACMUZsqXq  env-kill-934981  v1  2026-10-14 18:19:15
└── environment  env_01FpAB2qFcwu38Ux6WoPVtbv  (deleted)
    └── session     sesn_012ojM59ZgxnEcDsq5w3H4kM  idle  env-kill experiment  2026-10-14 18:19:15

agent  agent_01J2finEoCJCuPzu7mGqMPSx  env-inspector-7be53f  v1  2026-10-14 17:49:04
agent  agent_01BZnzZNDuvquti3mN7DmoBP  env-inspector-3f5580  v1  2026-10-14 17:47:11
agent  agent_01B3cLZ5Lvu4qCPAiyRyMcib  env-inspector-0a83c7  v1  2026-10-14 17:42:14
agent  agent_01LxZHGEEJSdPUJ3g3FJdgLw  SRE Agent  v1  2026-10-13 18:28:20
└── environment  env_01Wjq2pYAb2zQwU4NSVecfgq  sre-agent-e2e-5129b1
    └── session     sesn_01FQV1Nw4taDPcyT2Khq5rpB  idle    2026-10-13 18:28:25

agent  agent_01BNJHWBPXm4raNxCv2UUUyx  SRE Agent  v1  2026-10-13 04:28:24
agent  agent_01LttSXWHs7e9gtDTYEtiAQx  SRE Agent  v1  2026-10-12 05:26:54
agent  agent_01L9FqMHiRb6ZF61ZDEKVSG4  SRE Agent  v1  2026-10-12 05:25:06
environments with no sessions or deployments
├── environment  env_01Xdg2WJrsZaR5yDMNz778qh  sbx-kill-08b9c0  2026-10-14 19:07:57
├── environment  env_01Eh4yJMYe7BDqi7PUcGAsEp  sbx-kill-3e0dd5  2026-10-14 19:01:31
├── environment  env_01UNoQG6oEdEs1ADFdDKgEGD  sbx-kill-85b73c  2026-10-14 19:00:07
├── environment  env_01LpmRHzjSXFTxtZRB87Zifk  dep-kill-4a4462  2026-10-14 18:37:17
├── environment  env_01TM8DeGiDYP3ShCHXese2Ue  env-inspect-b06a37  2026-10-14 17:49:03
├── environment  env_01Cd2hJAu3z4WE9w95ajTgRS  env-inspect-919c8d  2026-10-14 17:47:10
├── environment  env_01FdZ12Xq8YjkfyS3TPE12sg  env-inspect-f1d064  2026-10-14 17:42:14
├── environment  env_01MJUmqdnBqnWgxTwcznNT2Z  sre-agent-6e86c9  2026-10-13 04:39:27
├── environment  env_01G2NQvixUpBpJSrJGLV93hW  sre-agent-e2e-2fcf5c  2026-10-12 05:26:54
└── environment  env_016TD2g2KHoDSQKVoxmopAgq  sre-agent-e2e-7f9d5c  2026-10-12 05:25:06

14 agents, 11 environments, 2 sessions, 0 deployments
```

**Reading it.**
- 14 agents: 10 from my test scripts, 4 `SRE Agent` from the workshop.
- 11 environments: 7 from my test scripts, 4 `sre-agent-*` from the workshop. Ten of the eleven appear in the last group because no session uses them.
- 2 sessions: the leftover `env-kill experiment` session, whose environment shows as `(deleted)`, and one session on a workshop SRE agent.
- 0 deployments. The one I created for testing was archived, and it does not appear. Archived items seem to be hidden from this listing.

## cleanup.py

**What it does.** Removes the resources my test scripts created, and nothing else. It only touches names starting with these prefixes, so the workshop's own `SRE Agent` and `sre-agent-*` resources are never listed:

`env-kill-`, `dep-kill-`, `sbx-kill-`, `env-inspect-`, `env-inspector-`

It is a dry run by default. With `--yes` it removes things in dependency order, because an environment cannot be deleted while sessions reference it:

1. Deployments, **archived**. This stops new sessions.
2. Sessions, deleted.
3. Environments, deleted.
4. Agents, **archived**.

It keeps going if one removal fails, and prints a count at the end.

**Run it.**

```bash
python my/cleanup.py          # dry run: list what would be removed
python my/cleanup.py --yes    # remove it
```

### Output of `cleanup.py --yes`

The script first prints what it found, then what it removed. I ran the dry run first and it listed the same 18 items.

```text
deployments: 0  sessions: 1  environments: 7  agents: 10
  session     sesn_012ojM59ZgxnEcDsq5w3H4kM  env-kill experiment
  environment env_01Xdg2WJrsZaR5yDMNz778qh  sbx-kill-08b9c0
  environment env_01Eh4yJMYe7BDqi7PUcGAsEp  sbx-kill-3e0dd5
  environment env_01UNoQG6oEdEs1ADFdDKgEGD  sbx-kill-85b73c
  environment env_01LpmRHzjSXFTxtZRB87Zifk  dep-kill-4a4462
  environment env_01TM8DeGiDYP3ShCHXese2Ue  env-inspect-b06a37
  environment env_01Cd2hJAu3z4WE9w95ajTgRS  env-inspect-919c8d
  environment env_01FdZ12Xq8YjkfyS3TPE12sg  env-inspect-f1d064
  agent       agent_01E1tbffo7jX7tAxqhrENrVb  sbx-kill-d683bc
  agent       agent_011FZ2a11rygvv85amk4DPe4  sbx-kill-f8e941
  agent       agent_01WWg2ou5ZJFEWY6VUESUKS3  sbx-kill-826991
  agent       agent_01C3FyJbv9YMVFDVvrgbXH53  dep-kill-b63165
  agent       agent_01RJFVVPxKDSdKoDU1hQTxLA  env-kill-0d77b2
  agent       agent_01Ce781pweUDAiLCx7ZN7mH3  env-kill-5eac6a
  agent       agent_01RzxFioiqmmN9kACMUZsqXq  env-kill-934981
  agent       agent_01J2finEoCJCuPzu7mGqMPSx  env-inspector-7be53f
  agent       agent_01BZnzZNDuvquti3mN7DmoBP  env-inspector-3f5580
  agent       agent_01B3cLZ5Lvu4qCPAiyRyMcib  env-inspector-0a83c7

  removed  session sesn_012ojM59ZgxnEcDsq5w3H4kM
  removed  environment env_01Xdg2WJrsZaR5yDMNz778qh
  removed  environment env_01Eh4yJMYe7BDqi7PUcGAsEp
  removed  environment env_01UNoQG6oEdEs1ADFdDKgEGD
  removed  environment env_01LpmRHzjSXFTxtZRB87Zifk
  removed  environment env_01TM8DeGiDYP3ShCHXese2Ue
  removed  environment env_01Cd2hJAu3z4WE9w95ajTgRS
  removed  environment env_01FdZ12Xq8YjkfyS3TPE12sg
  removed  agent agent_01E1tbffo7jX7tAxqhrENrVb
  removed  agent agent_011FZ2a11rygvv85amk4DPe4
  removed  agent agent_01WWg2ou5ZJFEWY6VUESUKS3
  removed  agent agent_01C3FyJbv9YMVFDVvrgbXH53
  removed  agent agent_01RJFVVPxKDSdKoDU1hQTxLA
  removed  agent agent_01Ce781pweUDAiLCx7ZN7mH3
  removed  agent agent_01RzxFioiqmmN9kACMUZsqXq
  removed  agent agent_01J2finEoCJCuPzu7mGqMPSx
  removed  agent agent_01BZnzZNDuvquti3mN7DmoBP
  removed  agent agent_01B3cLZ5Lvu4qCPAiyRyMcib

18 removed, 0 failed. (Deployments and agents are archived, not deleted.)
```

**Reading it.**
- It found 1 session, 7 environments and 10 agents, and removed all 18 with 0 failures.
- The leftover session could be deleted even though its environment was already gone.
- Agents and deployments are archived, not deleted.

## list-resources.py again, after cleanup

```text
agent  agent_01LxZHGEEJSdPUJ3g3FJdgLw  SRE Agent  v1  2026-10-13 18:28:20
└── environment  env_01Wjq2pYAb2zQwU4NSVecfgq  sre-agent-e2e-5129b1
    └── session     sesn_01FQV1Nw4taDPcyT2Khq5rpB  idle    2026-10-13 18:28:25

agent  agent_01BNJHWBPXm4raNxCv2UUUyx  SRE Agent  v1  2026-10-13 04:28:24
agent  agent_01LttSXWHs7e9gtDTYEtiAQx  SRE Agent  v1  2026-10-12 05:26:54
agent  agent_01L9FqMHiRb6ZF61ZDEKVSG4  SRE Agent  v1  2026-10-12 05:25:06
environments with no sessions or deployments
├── environment  env_01MJUmqdnBqnWgxTwcznNT2Z  sre-agent-6e86c9  2026-10-13 04:39:27
├── environment  env_01G2NQvixUpBpJSrJGLV93hW  sre-agent-e2e-2fcf5c  2026-10-12 05:26:54
└── environment  env_016TD2g2KHoDSQKVoxmopAgq  sre-agent-e2e-7f9d5c  2026-10-12 05:25:06

4 agents, 4 environments, 1 sessions, 0 deployments
```

## Summary

The raw before and after capture is also kept in [cleanup-comparison.md](cleanup-comparison.md).

| | Before | After | Removed |
|---|---|---|---|
| Agents | 14 | 4 | 10 |
| Environments | 11 | 4 | 7 |
| Sessions | 2 | 1 | 1 |
| Deployments | 0 | 0 | 0 |

- **It worked as designed.** Everything my test scripts made is gone from the listing. What remains is the workshop's own set: four `SRE Agent` agents, four `sre-agent-*` environments, and one session on an SRE agent.
- **The prefix filter held.** None of the workshop resources were removed.
- **Not deleted, only archived.** Agents and deployments are archived. They no longer appear in the listing, but they may still exist in the account. I have not checked.
- **Limits of the listing.** It cannot show archived items, so it cannot tell "archived" from "gone".
- **A habit worth keeping.** Run `python my/list-resources.py` before and after a batch of experiments. The test scripts leave an environment and an agent behind every run.

---

[Back to README](README.md) · Previous: [03 · Kill experiments](03-kill-experiments.md) · Next: [05 · Animation](05-animation.md)
