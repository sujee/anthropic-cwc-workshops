# Cleanup: before and after

Ran `python cleanup.py --yes`, then `python list-resources.py`. Captured 2026-10-14 19:24 UTC.

## What cleanup.py did

```text
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

## Before

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

## After

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
