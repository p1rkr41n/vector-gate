# [#65] Switch `parse_grok` to call `parse_groks`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/65)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2022-05-05T15:31:55Z`
- **Updated At**: `2026-06-16T13:11:06Z`
- **Comments**: 2
- **Labels**: `vrl:stdlib`, `type:tech debt`, `stdlib:parse_grok`, `stdlib:parse_groks`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/65)

---

## Description

Currently the `parse_grok` function differs in implementation from `parse_groks` (including different filter support). We are still working on some extensions to the standard grok patterns that are currently only in `parse_groks` but these are undocumented so far, so we can have `parse_grok` just call `parse_groks` since it is a strict superset of functionality.
