# Issue #129: Allow `else` keyword on newline in VRL

- **URL:** https://github.com/vectordotdev/vrl/issues/129
- **Author:** @jszwedko
- **Status:** CLOSED (completed)
- **Created:** 2021-03-31T13:29:08Z
- **Closed:** 2026-05-01T18:40:40Z
- **Labels:** type:enhancement, vrl:parser

## Description

Broken off from https://github.com/timberio/vector/pull/6893 and https://github.com/timberio/vector/issues/6848.

The user has a program that looks like:

```
if (starts_with(image, "k8s.gcr.io/kube-apiserver") ||
    starts_with(image, "k8s.gcr.io/kube-scheduler")) {"k8s-plain"}
else {"unknown"}
```

However, we don't allow `else` to appear on a newline by itself without the closing `}`.

We should consider allowing this.
