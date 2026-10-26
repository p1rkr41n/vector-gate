# [#109] Add `to_array` coercion function to VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/109)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2021-06-07T11:00:18Z`
- **Updated At**: `2026-06-01T14:16:26Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/109)

---

## Description

```coffee
to_array(null) # => []
to_array([]) # => []

# any other type results in an error
```

Currently, the same can be achieved using if conditions or (not exactly similar, but close) `array(.foo) ?? []`, but wanting to coerce a potential `null` value when working with arrays is a common enough occurrence to justify this function.

cc @leebenson
