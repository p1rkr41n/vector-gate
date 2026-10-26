# [#1105] `del` does not compact objects when the requested path does not exist

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1105)
- **Status**: `OPEN`
- **Author**: [@bruceg](https://github.com/bruceg)
- **Created At**: `2024-10-31T17:29:33Z`
- **Updated At**: `2026-06-16T13:09:48Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:del`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1105)

---

## Description

When using `del` with `compact: true`, [the docs say](https://vector.dev/docs/reference/vrl/functions/#del):
> After deletion, if `compact` is `true` and there is an empty object or array left, the empty object or array is also removed

However, if the path that is given does not exist, no compaction of the parents is done.

For example, given the VRL program `del(.foo.bar, compact: true)` and an input object of `{"foo": {"bar":true}}`, the result is an empty object. However, with an input object of `{"foo": {}}`, the result is unchanged, even though the implication is that `"foo"` would be compacted.
