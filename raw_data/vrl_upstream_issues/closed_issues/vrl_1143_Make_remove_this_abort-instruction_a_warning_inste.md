# Issue #1143: Make `remove this abort-instruction` a warning instead of an error

- **URL:** https://github.com/vectordotdev/vrl/issues/1143
- **Author:** @pront
- **Status:** CLOSED (completed)
- **Created:** 2024-11-26T15:41:50Z
- **Closed:** 2025-02-03T16:21:22Z
- **Labels:** vrl:compiler

## Description

Example:

```
2024-11-26T07:20:11.641948Z ERROR vector::topology::builder: Configuration error. error=Transform "filter_metrics":
error[E620]: can't abort infallible function
  ┌─ :1:1
  │
1 │ match!(to_string(.name) ?? "default", r'^(cpu.*|kong.*|mem.*)')
  │ ^^^^^- remove this abort-instruction
  │ │
  │ this function can't fail
  │
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

Relaxing the above to be a warning is a backwards compatible change which I believe will make VRL easier to use. 
