# Issue #1275: VRL REPL doesn't parse "\u" neither "\x" escapes

- **URL:** https://github.com/vectordotdev/vrl/issues/1275
- **Author:** @ulidtko
- **Status:** CLOSED (completed)
- **Created:** 2025-02-17T08:22:35Z
- **Closed:** 2025-02-18T17:35:13Z
- **Labels:** None

## Description

Hi! Per my reading of https://vector.dev/docs/reference/vrl/expressions/#string this should work:

```
$ "\u001b[95m Hello, string literals?"

error[E202]: syntax error
  ┌─ :1:1
  │
1 │ "\u001b[95m Hello, string literals?"
  │ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ unexpected error: invalid escape character: \u
  │
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

as well as `"`-string literal with `\x` escape:

```
$ "\x33"

error[E202]: syntax error
  ┌─ :1:1
  │
1 │ "\x33"
  │ ^^^^^^ unexpected error: invalid escape character: \x
  │
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

Yet, both give `syntax error` in the REPL.

### Version

`vector 0.44.0 (x86_64-unknown-linux-gnu 3cdc7c3 2025-01-13 21:26:04.735691656)`
