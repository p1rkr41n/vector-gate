# [#582] VRL function fallibility is dependant on argument types

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/582)
- **Status**: `OPEN`
- **Author**: [@jorgebay](https://github.com/jorgebay)
- **Created At**: `2023-02-22T12:38:50Z`
- **Updated At**: `2026-06-01T14:06:29Z`
- **Comments**: 8
- **Labels**: `vrl:compiler`, `vrl:typedef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/582)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

The built-in functions to coerce values can be both fallible and not fallible depending on the value.

The functions [are documented as fallible](https://vector.dev/docs/reference/vrl/functions/#coerce-functions) but if the compiler can detect that the value is of a certain type, it changes the signature from fallible to not fallible.

For example, this is a valid syntax and compiles:

```rust
str = "something"
result, err = to_bool(str)
```

But this fails:

```rust
b = false
result, err = to_bool(b)
```

with

```
error[E104]: unnecessary error assignment
  ┌─ :1:9
  │
1 │ result, err = to_bool(b)
  │ ------  ^^^   ---------- because this expression can't fail
  │ │       │
  │ │       this error assignment is unnecessary
  │ use: result = to_bool(b)
```

The same occurs with `to_float()`, `to_int()`, ...

The signature changes from:
```rust
to_bool(value: <boolean | integer | float | null | string>)
:: <boolean> , <error>
```

to:

```rust
to_bool(value: <boolean>) :: <boolean> // not fallible
```

As a language user this can be confusing, a function should not change fallibility depending on the parameter value.

### Configuration

_No response_

### Version

0.27

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
