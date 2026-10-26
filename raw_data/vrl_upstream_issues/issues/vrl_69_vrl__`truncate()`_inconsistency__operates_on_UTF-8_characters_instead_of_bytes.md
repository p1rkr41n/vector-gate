# [#69] vrl: `truncate()` inconsistency: operates on UTF-8 characters instead of bytes

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/69)
- **Status**: `OPEN`
- **Author**: [@hhromic](https://github.com/hhromic)
- **Created At**: `2022-04-22T15:09:57Z`
- **Updated At**: `2026-06-16T13:11:09Z`
- **Comments**: 4
- **Labels**: `vrl:stdlib`, `stdlib:truncate`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/69)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I'm not sure if this is a bug or a feature request. I tend to consider it a bug due to consistency expectations.

String manipulation functions in VRL seem to mostly operate on bytes and not UTF-8 characters (unicode scalars).

This was recently brought up for some discussion for the `length()` function in https://github.com/vectordotdev/vector/issues/12019, where a new `strlen()` was implemented to operate on UTF-8 characters instead of bytes.

However, I just noticed that the `truncate()` function is operating in UTF-8 characters instead of bytes, creating an inconstency.

This is problematic for us because we use `truncate()` to limit the number of bytes in a field that later is used for insertion into a `VARCHAR(size)` column in an SQL database, which defines `size` in bytes (highly likely an SQL standard).

Consider the following REPL examples:
```
$ truncate(s'hello', 2)
"he"

$ length(truncate(s'hello', 2))
2

$ truncate(s'ñandú', 2)  # expected just 'ñ' here due to using 2 bytes
"ña"

$ length(truncate(s'ñandú', 2))  # expected 2 here
3
```

For completeness, I checked up the `slice()` function and indeed operates on bytes as expected, like `length()`:
```
$ length(s'ñandú')
7

$ slice!(s'ñandú', 0)
"ñandú"

$ slice!(s'ñandú', 1)
"�andú"

$ slice!(s'ñandú', 2)
"andú"

$ slice!(s'ñandú', 3)
"ndú"

$ slice!(s'ñandú', 4)
"dú"

$ slice!(s'ñandú', 5)
"ú"

$ slice!(s'ñandú', 6)
"�"

$ slice!(s'ñandú', 7)
""

$ slice!(s'ñandú', 8)
function call error for "slice" at (0:21): "start" must be between "-7" and "7"
```

Fixing this is probably going to be tricky because of the obvious breakage :(

### Configuration

_No response_

### Version

vector 0.21.0 (x86_64-unknown-linux-gnu c1edb89 2022-04-14)

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
