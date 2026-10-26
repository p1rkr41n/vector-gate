# [#113] Unresolvable VRL compiler complaint about fallibility

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/113)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2021-05-12T15:51:11Z`
- **Updated At**: `2026-06-01T14:04:47Z`
- **Comments**: 2
- **Labels**: `vrl:diagnostic`, `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/113)

---

## Description

Discovered by a user.

Version: `vector 0.13.0 (v0.13.0 x86_64-apple-darwin 2021-04-21)`

I whittled down the reproducible case to:

```toml
[sources.in]
type = "stdin"

[transforms.remap]
  type = "remap"
  inputs = ["in"]
  source = '''
  foo, foo_err = parse_regex("hello 123 world", r'(?P<bar>\d+)')
  if foo_err != null {
    bar, bar_err = parse_regex("hello 123 world", r'(?P<bar>\d+)')
    if bar_err != null {
      log(bar_err)
    } else {
      .line = merge(.line, bar)
    }
  } else {
    .line = merge(.line, foo)
  }
  '''

[sinks.out]
type = "console"
inputs = ["remap"]
encoding.codec = "json"
```

If you run `vector --config` with this, it gives:

```
error[E103]: unhandled fallible assignment
   ┌─ :10:13
   │
10 │     .line = merge(.line, foo)
   │     ------- ^^^^^^^^^^^^^^^^^
   │     │       │
   │     │       this expression is fallible
   │     │       update the expression to be infallible
   │     or change this to an infallible assignment:
   │     .line, err = merge(.line, foo)
   │
   = see documentation about error handling at https://errors.vrl.dev/#handling
   = learn more about error code 103 at https://errors.vrl.dev/103
   = see language documentation at https://vrl.dev
```

If we resolve this by adding `!` to the `merge` calls we see:

```
error[E620]: can't abort infallible function
   ┌─ :10:13
   │
10 │     .line = merge!(.line, foo)
   │             ^^^^^- remove this abort-instruction
   │             │
   │             this function can't fail
   │
   = see documentation about error handling at https://errors.vrl.dev/#handling
   = see language documentation at https://vrl.dev
```
