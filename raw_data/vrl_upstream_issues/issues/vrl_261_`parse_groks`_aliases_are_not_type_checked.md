# [#261] `parse_groks` aliases are not type checked

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/261)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2023-05-26T19:02:16Z`
- **Updated At**: `2026-06-16T13:10:29Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`, `crash`, `stdlib:parse_groks`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/261)

---

## Description

The following VRL code will panic. The 3rd argument is an object containing grok aliases. Each value should be a string, but the `parse_groks` function fails to check this.

```coffee
parse_groks!("", [], {"foo": 3})
```

VRL version: `main` (ebb1f2b739e776)
