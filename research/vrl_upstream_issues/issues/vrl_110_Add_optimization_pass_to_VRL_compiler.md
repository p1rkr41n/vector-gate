# [#110] Add optimization pass to VRL compiler

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/110)
- **Status**: `OPEN`
- **Author**: [@lukesteensen](https://github.com/lukesteensen)
- **Created At**: `2021-05-28T16:19:39Z`
- **Updated At**: `2023-03-28T14:12:38Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/110)

---

## Description

We added the `match_any` function in vectordotdev/vector#7414 to allow for improved performance when matching a single field against multiple regular expressions. This was in response to an issue with a relatively slow `match(.foo, ...) || match(.foo, ...) || ...`.

An alternative to adding new functions that are more performant in certain cases would be to identify those patterns at compile time and transform them into a more efficient form internally. This would require some kind of pattern-matching optimization pass in the VRL compiler.
