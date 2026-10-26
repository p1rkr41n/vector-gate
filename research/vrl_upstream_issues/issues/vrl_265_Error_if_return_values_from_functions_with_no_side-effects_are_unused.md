# [#265] Error if return values from functions with no side-effects are unused

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/265)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2023-06-14T22:21:29Z`
- **Updated At**: `2023-10-20T20:00:43Z`
- **Comments**: 2
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/265)

---

## Description

A user was recently confused because they had a VRL program that they thought would update metrics tags, but it didn't because they forgot to assign the result of a `merge` function call. They had:

```
merge(.tags, {"tag": "youreit"})
```

When they should have had

```
.tags = merge(.tags, {"tag": "youreit"})
```

To help users avoid this sort of issue, I think it'd be useful for the compiler to raise an error if the result of a VRL function that has no side-effects is not used. The `#[must_use]` Rust macro could be some inspiration.
