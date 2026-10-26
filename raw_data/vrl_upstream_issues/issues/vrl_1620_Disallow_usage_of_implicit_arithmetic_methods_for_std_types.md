# [#1620] Disallow usage of implicit arithmetic methods for std types

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1620)
- **Status**: `OPEN`
- **Author**: [@thomasqueirozb](https://github.com/thomasqueirozb)
- **Created At**: `2026-02-02T15:26:14Z`
- **Updated At**: `2026-02-02T15:26:14Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1620)

---

## Description

Implicit arithmetic methods like `*`, `/`, `+`, `-` can sometimes have code that can panic. Ideally we should never use those as they can create code that panics with 0 indication that it does.

Bug: #1615
See: #1618
