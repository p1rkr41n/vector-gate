# [#122] Implement a bit-test function within VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/122)
- **Status**: `OPEN`
- **Author**: [@aphelps](https://github.com/aphelps)
- **Created At**: `2021-04-22T21:00:26Z`
- **Updated At**: `2026-06-01T14:16:21Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/122)

---

## Description

### Current Vector Version
```
vector 0.12.2 (v0.12.2 x86_64-unknown-linux-gnu 2021-03-30)
```

### Use-cases

We have logs that make use of a bit-flag field to indicate various states, for which we would like to use the `route` transform to split into multiple streams.

### Attempted Solutions

Currently I believe I'd need to use the `lua` transform to test for bits in an integer field and convert those to separate named boolean values, and then use the `route` transform to test for those fields with the `exists()` function.

### Proposal

This could either be done via an explicit function, ie `test_bit(value: <integer>, bit: <integer>) :: <boolean>` or use the typical bit manipulation syntax from Rust, ie `<integer> & <integer>` or `<integer> & (1 << <integer>)` depending on how fancy you want to make it.  But really the simple `test_bit()` option would be fine for my use case.

### References

NA
