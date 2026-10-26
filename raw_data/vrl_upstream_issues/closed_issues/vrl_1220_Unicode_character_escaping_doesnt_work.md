# Issue #1220: Unicode character escaping doesn't work

- **URL:** https://github.com/vectordotdev/vrl/issues/1220
- **Author:** @simplepad
- **Status:** CLOSED (not_planned)
- **Created:** 2025-01-14T07:36:04Z
- **Closed:** 2025-01-14T19:18:35Z
- **Labels:** vrl:compiler

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Using `\u{7FFF}` to insert unicode characters into a string literal doesn't work.
Copying the second example from https://vector.dev/docs/reference/vrl/expressions/#string-examples into VRL playground like so `.test = "Hello, world! \u1F30E"` results in an error:
```
error[E202]: syntax error
  ┌─ :1:1
  │
1 │ .test = "Hello, world! \u1F30E"
  │ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ unexpected error: invalid escape character: \u
  │
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```
 

### Configuration

_No response_

### Version

version 0.43.1 (x86_64-unknown-linux-gnu)

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
