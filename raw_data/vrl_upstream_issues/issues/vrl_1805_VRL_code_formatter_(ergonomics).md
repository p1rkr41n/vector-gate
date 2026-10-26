# [#1805] VRL code formatter (ergonomics)

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1805)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2026-06-06T19:42:58Z`
- **Updated At**: `2026-07-08T18:11:51Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1805)

---

## Description

A canonical formatter for VRL — similar to `gofmt` or `rustfmt` — that enforces a single standard style.

## Proposed interface

This is the minimum viable interface to start:

\`\`\`bash
vrl fmt file.vrl          # format in place
vrl fmt --check file.vrl  # exit non-zero if unformatted (CI)
\`\`\`

## Initial formatting rules (opinionated, not configurable)

- 4-space indentation
- Spaces around binary operators
- Comments preserved as-is

This keeps the initial scope small. We will revisit rules as we gather feedback from the community — contributions are welcome!
