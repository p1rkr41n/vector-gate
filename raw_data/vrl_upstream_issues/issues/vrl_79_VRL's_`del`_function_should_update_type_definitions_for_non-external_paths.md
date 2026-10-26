# [#79] VRL's `del` function should update type definitions for non-external paths

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/79)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-02-08T12:28:50Z`
- **Updated At**: `2026-06-16T13:11:15Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `vrl:typedef`, `stdlib:del`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/79)

---

## Description

This works as expected:

```coffee
.foo.bar = "baz"
del(.foo.bar)
string!(.foo.bar)
```

```
function call error for "string" at (0:17): expected "string", got "null"
```

This does not:

```coffee
foo.bar = "baz"
del(foo.bar)
string!(foo.bar)
```

```
error[E620]: can't abort infallible function
  ┌─ :1:1
  │
1 │ string!(foo.bar)
  │ ^^^^^^- remove this abort-instruction
  │ │
  │ this function can't fail
  │
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = see language documentation at https://vrl.dev
```

The problem is that the `del` function uses the `update_state` call: https://github.com/vectordotdev/vector/blob/f049246db7e3025aa55eb1e160bd3669b485887d/lib/vrl/stdlib/src/del.rs#L172-L178

This then calls `delete_type_def`: https://github.com/vectordotdev/vector/blob/ee6771146836c53cd13f8260b29bc678e61b6330/lib/vrl/compiler/src/expression/query.rs#L53-L62

Which is only implemented to work for external targets, whereas the second example above works on an internal target (variable `foo`).

