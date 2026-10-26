# [#90] `to_timestamp` can fail if numeric values are too big

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/90)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2021-10-06T21:29:07Z`
- **Updated At**: `2026-06-01T14:05:06Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/90)

---

## Description

Reported by [user in discord](https://discord.com/channels/742820443487993987/764187584452493323/895385025854451782).

`to_timestamp(999999999999999999999.1)` is not identified by VRL as fallible, but does actually fail with:

```
function call error for "to_timestamp" at (0:38): unable to coerce 1000000000000000000000 into "timestamp"
```
