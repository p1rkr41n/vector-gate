# [#137] Add function memoization

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/137)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2021-01-19T20:08:36Z`
- **Updated At**: `2026-06-01T14:16:15Z`
- **Comments**: 3
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/137)

---

## Description

There have been several situations in which a VRL function has relatively slow runtime performance, but the operation it performs results in a value that is relatively static.

see: https://github.com/timberio/vector/pull/6141

I propose we add a “function cache” to the VRL runtime.

The idea is this:

- We add a new `state::FunctionCache` object.
- Functions have access to their own piece of this cache, namespaces by the function identifier (to start)
- They can store a `Value` type in the cache to fetch when needed.
- We either implement a TTL in the cache, or a “query counter”. Alternatively we leave cache invalidation up to the function.

There are still some things to work out here, but it seems a valuable property to have in the runtime.
