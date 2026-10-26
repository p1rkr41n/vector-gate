# [#268] Improve diagnostics from function fallibility caused by arguments

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/268)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2023-06-16T18:24:04Z`
- **Updated At**: `2023-06-16T18:24:04Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:diagnostic`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/268)

---

## Description

There has been quite a bit of confusion around functions being marked as fallible (when the function itself is considered infallible) due to an argument that may be an incorrect type. Improved compiler diagnostics pointing out that the issue is with a specific argument will probably help a lot here.

Example: https://github.com/vectordotdev/vrl/issues/267#issue-1761022044
