# [#1154] VRL error message for field assignment to non-object has a one-off typo in it

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1154)
- **Status**: `OPEN`
- **Author**: [@bruceg](https://github.com/bruceg)
- **Created At**: `2024-11-30T00:02:41Z`
- **Updated At**: `2026-06-01T14:08:11Z`
- **Comments**: 0
- **Labels**: `vrl:diagnostic`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1154)

---

## Description

Given the VRL code:
```
foo = {}
foo.bar.baz = 12
```
the error message suggestions are missing the leading `.`:
```
error[E642]: parent path segment rejects this mutation
  ┌─ :2:9
  │
2 │ foo.bar.baz = 12
  │ ------- ^^^ querying a field of a non-object type is unsupported
  │ │
  │ this path resolves to a value of type undefined
  │
  = try: change parent value to object, before assignment
  =
  =     foobar = {}
  =     foobar.baz = 12
```
