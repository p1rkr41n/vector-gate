# [#99] VRL: strange path creation due to double quotes

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/99)
- **Status**: `OPEN`
- **Author**: [@spencergilbert](https://github.com/spencergilbert)
- **Created At**: `2021-08-06T14:21:27Z`
- **Updated At**: `2026-06-01T14:04:56Z`
- **Comments**: 0
- **Labels**: `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/99)

---

## Description

Consider the following VRL:

```vrl
$ .nested.""field"" = "foobar"
"foobar"

$ .
{ "nested": { "": { "field": { "": "foobar" } } } }
```

This could arguably be either a syntax error, or possible create a path like `.nested."field"` or even `.nested.""field""` (or any assortment of escaped chars...

I wouldn't expect the current behavior.
