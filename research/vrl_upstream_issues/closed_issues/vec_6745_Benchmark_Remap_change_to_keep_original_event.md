# Issue #6745: Benchmark Remap change to keep original event

- **URL:** https://github.com/vectordotdev/vector/issues/6745
- **Author:** @JeanMertz
- **Status:** CLOSED (completed)
- **Created:** 2021-03-12T15:43:11Z
- **Closed:** 2022-12-28T16:34:02Z
- **Labels:** domain:vrl, transform:remap

## Description

We (read: I) merged the change in https://github.com/timberio/vector/pull/6719 without doing any benchmarking to see the impact on performance.

We should measure the impact here, to make sure we're not causing a big drop in performance.

Two things to note here:

- Mutating the event partially when a program fails seems to be something we don't want to have as a default, so the change in that PR still seems to be something we want.
- If a program cannot fail (we can guarantee this at compile/boot-time), _or_ if `drop_on_error` is set to `true` (defaults to `false`), then we don't clone the original event, so there shouldn't be any drop in performance in those cases.
- In any other case, we now keep a copy of the original event for when we need to revert it if the program fails at runtime.

I assigned @jszwedko as I'm not available next week, but anyone else can pick this up as well, or I can do the benchmarking once I'm available again.

