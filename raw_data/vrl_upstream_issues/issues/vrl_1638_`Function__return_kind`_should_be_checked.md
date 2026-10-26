# [#1638] `Function::return_kind` should be checked

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1638)
- **Status**: `OPEN`
- **Author**: [@thomasqueirozb](https://github.com/thomasqueirozb)
- **Created At**: `2026-02-13T16:21:13Z`
- **Updated At**: `2026-02-13T16:21:13Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1638)

---

## Description

(at least) when running tests and maybe also when running VRL in debug mode, we should check that the function's return actually matches `return_kind`, much like what is done for `Parameter::kind`.

Ref: #1628
