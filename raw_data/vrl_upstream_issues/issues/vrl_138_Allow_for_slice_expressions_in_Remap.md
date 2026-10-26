# [#138] Allow for slice expressions in Remap

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/138)
- **Status**: `OPEN`
- **Author**: [@binarylogic](https://github.com/binarylogic)
- **Created At**: `2021-01-15T20:30:03Z`
- **Updated At**: `2023-03-28T14:34:52Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/138)

---

## Description

An expression to slice values would make transforming values easier.

## Examples

```
.message[1:10]
.array[0:2]
```

## Requirements

- [ ] Ability to slice strings
- [ ] Ability to slice arrays
- [ ] Allow for negative indexing
