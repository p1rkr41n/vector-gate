# [#67] Dedicated dynamic path query syntax in VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/67)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-05-03T11:23:17Z`
- **Updated At**: `2026-06-01T14:16:43Z`
- **Comments**: 1
- **Labels**: `vrl:compiler`, `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/67)

---

## Description

_This issue got spun out from [this comment](https://github.com/vectordotdev/vector/pull/8467#issuecomment-1086785291)._

Dynamic field access in VRL is currently supported through the `get` function.

We want to remove this function in favour of dedicated syntax to achieve the same result.

Specifically, we would like to allow this:

```coffee
idx = 12
bar = "baz"
.foo."{{bar}}"[idx]
```

That is, we'll use string-templating (see vectordotdev/vector#8467) to allow dynamic fields, and allow variables (that _must_ resolve to a number) inside `[...]` for array indexing.
