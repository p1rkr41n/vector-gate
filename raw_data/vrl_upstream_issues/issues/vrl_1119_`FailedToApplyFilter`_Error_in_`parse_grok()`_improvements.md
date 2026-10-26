# [#1119] `FailedToApplyFilter` Error in `parse_grok()` improvements

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1119)
- **Status**: `OPEN`
- **Author**: [@neuronull](https://github.com/neuronull)
- **Created At**: `2024-11-11T15:34:53Z`
- **Updated At**: `2026-06-16T13:09:46Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `type:tech debt`, `stdlib:parse_grok`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1119)

---

## Description

During #1113 , some changes were proposed to the Error types and it was observed that the FailedToApply filter covers a lot of distinct cases and also hides the underlying error.

We should consider:
- surfacing the underlying error
- expanding the catch all type to distinct variants that cover each scenario.
