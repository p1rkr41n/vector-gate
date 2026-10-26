# [#130] Add headers for `parse_csv`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/130)
- **Status**: `OPEN`
- **Author**: [@vladimir-dd](https://github.com/vladimir-dd)
- **Created At**: `2021-03-29T10:20:03Z`
- **Updated At**: `2026-06-16T13:11:39Z`
- **Comments**: 3
- **Labels**: `vrl:stdlib`, `stdlib:parse_csv`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/130)

---

## Description

As a follow-up on vectordotdev/vector#5371 we should add an option to set headers for the `parse_csv` function, for example:
```
parse_csv!("foo,bar", headers: ["header1", "header2"])
// { "header1": "foo", "header2": "bar" }
```
