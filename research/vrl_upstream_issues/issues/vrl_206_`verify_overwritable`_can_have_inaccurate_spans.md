# [#206] `verify_overwritable` can have inaccurate spans

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/206)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2023-04-27T11:53:38Z`
- **Updated At**: `2026-06-01T14:06:38Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/206)

---

## Description

`verify_overwritable` is used to ensure VRL assignments can only assign to types that make sense, for example you can't assign to an index of an object. When doing this check, spans (for error messages) are calculated by taking the overall span for the path, and subtracting segments based on the string length of the `Display` implementation of `OwnedSegment`. The length here isn't guaranteed to match (mostly do to escaping / quoting), so the span can be inaccurate. A simple case to reproduce is to try to use an invalid assignment with a path that unnecessarily quotes a segment.

When this was originally introduced, it caused a runtime panic (https://github.com/vectordotdev/vector/issues/13461), and was fixed by using `saturating_sub` to prevent underflows. This prevents panics, but didn't actually solve the root cause. A different approach should be taken here.
