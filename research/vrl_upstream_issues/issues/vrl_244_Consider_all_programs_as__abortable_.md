# [#244] Consider all programs as "abortable"

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/244)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2023-05-13T01:58:36Z`
- **Updated At**: `2023-06-29T14:53:36Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/244)

---

## Description

Today, a `Program` can provide information about whether it's possible to fail (`fallible`) or abort (`abortable`). It may be reasonable to just assume any program can potentially abort, and remove the `abortable` field from `ProgramInfo`. aborts can be useful outside of an explicit abort. For example, when compiled to WASM, functions abort if they are unsupported in WASM. Programs could also potentially abort in the future as a protection against excessive memory or cpu usage (trying to create a very large array), or in cases that may cause a stack overflow.
