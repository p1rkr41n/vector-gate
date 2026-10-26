# [#1799] `resolve_constant` on function arguments is unsound/not deterministic when earlier arguments have side effects

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1799)
- **Status**: `OPEN`
- **Author**: [@thomasqueirozb](https://github.com/thomasqueirozb)
- **Created At**: `2026-06-04T17:34:13Z`
- **Updated At**: `2026-06-08T17:03:41Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1799)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

Several stdlib functions call `resolve_constant(state)` on one of their named arguments at compile time to constant-fold the value into the compiled `FunctionExpression`. For example, `match` freezes the pattern at compile time when it resolves to a constant, so the following program silently returns the wrong result:

```vrl
pat = r'foo';
match({ pat = r'bar'; "bar" }, pat)
# returns false — frozen compile-time pattern r'foo' does not match "bar"
# expected true  — runtime value of pat is r'bar', which matches "bar"
```

## Explanation

`resolve_constant` returns `Some` for a `Variable` whenever the compiler's type state records a constant value for that variable at compile time. The folded value is then frozen into the compiled expression and never re-evaluated at runtime.

This is unsound because VRL functions have no defined argument evaluation order. Each function's `resolve` implementation evaluates arguments in whatever internal order it chooses. `match` always evaluates `value` before `pattern` at runtime.

https://github.com/vectordotdev/vrl/blob/v0.33.1/src/stdlib/match.rs#L115-L118

the block in the first argument runs first and mutates `pat` before `pattern` would normally be read, but because `pat` was a deemed a compile-time constant it was already frozen and the runtime value is never consulted.

## Possibly affected functions

`chunks`, `crc`, `decrypt`, `del`, `encode_gzip`, `encode_zlib`, `encrypt`, `flatten`, `hmac`, `http_request`, `ip_cidr_contains`, `match`, `match_any`, `mod_func`, `parse_etld`, `parse_groks`, `random_bytes`, `random_float`, `random_int`, `redact`, `xxhash`, and the shared `util` helpers.

## Root cause

VRL named-argument calls have no defined evaluation order. Unlike positional arguments in languages like Rust (left-to-right), there is no contract, neither in the language specification nor enforced by the compiler, that guarantees the order in which a function's arguments are resolved at runtime. Each `FunctionExpression::resolve` implementation defines its own implicit order. Callers of `resolve_constant` therefore operate on a snapshot of compile-time state that may not reflect the state at the point the argument would actually be evaluated.

## What a proper fix would require

Either:

1. **Define a canonical evaluation order** for named function arguments (e.g. always evaluate all arguments in source order before dispatching to the function body), and enforce it uniformly — making cross-argument side effects predictable. Then `resolve_constant` would only be sound for arguments that are provably evaluated before any argument that could mutate them.

2. **Restrict `resolve_constant` to side-effect-free expressions** — i.e. only allow constant-folding for expressions that structurally cannot be affected by side effects (`Literal` variants, constant-folded pure operations on literals). Variables would never qualify regardless of their compile-time value.

Both options are non-trivial and touch the language design layer.

### VRL Program

```text

```

### VRL and/or Vector Version

VRL 0.33.1

### Debug Output

```text

```

### Example

_No response_

### Additional Context

_No response_

### References

_No response_
