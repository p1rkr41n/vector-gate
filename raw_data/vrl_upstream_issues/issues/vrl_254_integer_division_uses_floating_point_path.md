# [#254] integer division uses floating point path

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/254)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2023-05-23T20:18:02Z`
- **Updated At**: `2026-06-01T14:06:54Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/254)

---

## Description

integer division internally uses floating point math, which can cause precision issues for larger number.
Below is an example dividing a large number by 1, where the result loses several digits of precision. This should probably use integer math to be consistent with multiplication / addition / subtraction.

```coffee
$ 9223372036854775807 / 1
9223372036854776000
```
