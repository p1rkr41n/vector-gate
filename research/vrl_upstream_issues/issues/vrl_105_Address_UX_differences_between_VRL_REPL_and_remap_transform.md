# [#105] Address UX differences between VRL REPL and remap transform

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/105)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2021-07-12T08:54:07Z`
- **Updated At**: `2023-03-28T14:05:26Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `Epic`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/105)

---

## Description

Specifically, assigning a value to a target results in the compiler knowing the type of that value, which means error handling isn't needed (and in fact, is rejected), whereas at runtime in the remap transform, the value type might be unknown, which causes the program tested in the REPL not to be valid in the Remap transform.

I don't think we should "just" make the REPL forget types of assigned values, but I'm also not sure yet that the correct solution is. We'll have to experiment a bit to find the right balance.
