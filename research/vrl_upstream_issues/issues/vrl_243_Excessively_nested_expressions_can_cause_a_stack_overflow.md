# [#243] Excessively nested expressions can cause a stack overflow

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/243)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2023-05-13T01:50:48Z`
- **Updated At**: `2026-06-01T14:06:52Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`, `fuzz`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/243)

---

## Description

For example, negating a variable ~30,000 times will cause a stack overflow. I'll spare your eyes by not pasting a full example below. This isn't something that an end user is likely to type in, but guarding against this can be useful for cases where you are running un-trusted VRL code.
