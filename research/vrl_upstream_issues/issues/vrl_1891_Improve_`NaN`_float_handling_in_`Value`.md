# [#1891] Improve `NaN` float handling in `Value`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1891)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-02-03T18:06:08Z`
- **Updated At**: `2026-08-06T15:34:44Z`
- **Comments**: 4
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1891)

---

## Description

The original "Vector" `Value` contained an `f64`, but the "VRL" `Value` contained a `NotNan<f64>`. This lead to some interesting edge cases when converting between the two, which were relatively hidden.

When converting from a "Vector" Value to a "VRL" Value, 
https://github.com/vectordotdev/vector/blob/9c33519ddaaeee7c11f838f9d33dd31ab7294b86/lib/vector-core/src/event/value.rs#L321-L337

this utilizes the `From` impl to convert an `f64` to  a "VRL" Value.
https://github.com/vectordotdev/vector/blob/9c33519ddaaeee7c11f838f9d33dd31ab7294b86/lib/vrl/compiler/src/value/convert.rs#L182-L191

This implementation silently replaces `NaN` with `0.0`.

We should determine if/where in Vector `NaN` should be supported, and make this consistent in the code.


