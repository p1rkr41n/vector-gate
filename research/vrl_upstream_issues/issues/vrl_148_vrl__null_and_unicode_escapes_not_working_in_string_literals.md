# [#148] vrl: null and unicode escapes not working in string literals

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/148)
- **Status**: `OPEN`
- **Author**: [@hhromic](https://github.com/hhromic)
- **Created At**: `2022-03-21T21:36:38Z`
- **Updated At**: `2026-06-01T14:05:20Z`
- **Comments**: 23
- **Labels**: `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/148)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I recently found out that the null and unicode character escape sequences are not working in [string literal expressions in VRL](https://vector.dev/docs/reference/vrl/expressions/#string).
The documentation makes sense, therefore I think something is off in the VRL parser.

Examples from the VRL REPL:
```
$ "hello\0world"
error[E202]: syntax error
  ┌─ :1:1
  │
1 │ "hello\0world"
  │ ^^^^^^^^^^^^^^ unexpected error: invalid escape character: \0
  │
  = see language documentation at https://vrl.dev
```
```
$ "hello\u{1F30E}world"  # also tested with \U{1F30E} and \u1F30E just in case
error[E202]: syntax error
  ┌─ :1:1
  │
1 │ "hello\u{1F30E}world"
  │ ^^^^^^^^^^^^^^^^^^^^^ unexpected error: invalid escape character: \u
  │
  = see language documentation at https://vrl.dev
```

All the other documented escape sequences seems to be working fine (although not all printed correctly):
```
$ "hello\nworld"
"hello\nworld"

$ "hello\"world"
"hello\"world"

$ "hello\'world"
"hello'world"

$ "hello\\world"
"hello\\world"

$ "hello\nworld"
"hello\nworld"

$ "hello\rworld"  # \r (carriage-return) was rendered instead of printed with an escape
world"

$ "hello\tworld"  # \t (tab) was rendered instead of printed with an escape
"hello  world"
```

### Configuration

```text
N/A
```


### Version

vector 0.20.0 (x86_64-unknown-linux-gnu 2a706a3 2022-02-11)

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
