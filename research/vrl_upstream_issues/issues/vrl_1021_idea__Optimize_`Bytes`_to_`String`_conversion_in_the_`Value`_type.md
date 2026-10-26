# [#1021] idea: Optimize `Bytes` to `String` conversion in the `Value` type

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1021)
- **Status**: `OPEN`
- **Author**: [@bruceg](https://github.com/bruceg)
- **Created At**: `2024-09-06T15:05:02Z`
- **Updated At**: `2024-09-06T15:05:02Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:typedef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1021)

---

## Description

The VRL type `enum Value` uses `bytes::Bytes` as its store of string values, since the originating data may not in fact be valid UTF-8 strings. However, we frequently want to _use_ these bytes as a string, which leads to repeated calls to `String::from_utf8_lossy` on these bytes value. It may be preferable to avoid repeating this conversion by caching the result in some form in a new `Bytes` wrapper type.

While discussing this idea, we came up with several possible ways of doing this:

0. Add an additional `Value::String` variant for when we can prove the source data is a valid `String`. This, unfortunately, breaks all kinds of assumptions about the `Bytes` variant being the only place string data is stored, and so is most likely to lead to bugs.
1. Make a new `Bytes` enum and parse the incoming bytes when it is created to determine if it is valid UTF-8 or not. Conversion from `str` values would, of course, not need parsing and could be stored directly. Replace calls to `String::from_utf8_lossy(&bytes)` with new member functions on that type that intelligently return without re-parsing the data.
2. Make a new `Bytes` struct containing a `OnceLock` or `ArcSwap` sidecar to store the cached value of the conversion that will be initialized on demand instead of at creation time (except for when the source is statically known to be a valid string, of course). Replace calls as above. Note that we can't use a straight `Option` to cache the conversion as that would require any function using `Bytes` to borrow the value mutably which will require far too many code changes and may even be impossible where multiple immutable borrows are required.

Since most values that will be stored in the `Bytes` variant will be valid UTF-8 strings, there was some debate over whether storing the resulting conversion in the case of invalid bytes would be worth the overhead of the additional data size. The `Bytes` is already the largest variant in the `Value` type and any addition to its size will grow memory requirements, and so must be considered carefully.

It would be good to spend some time profiling how often this conversion happens and benchmarking to ensure the benefits are not outweighed by the additional memory overheads. However, the string conversions are scattered throughout the code bases, making it very difficult to identify any of them as a hot spot. One thought for profiling would be to set up counters for how often `Bytes` are created and converted and then log these values before exit.

Work on this idea has started in [the `bruceg/vrl-bytes-idea` branch](https://github.com/vectordotdev/vrl/tree/bruceg/vrl-bytes-idea). Expect this to be rebased frequently if any further progress is made.
