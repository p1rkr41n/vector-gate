# [#1536] parse_key_value failed when string ends with delimiter

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1536)
- **Status**: `OPEN`
- **Author**: [@alexeynl](https://github.com/alexeynl)
- **Created At**: `2025-10-14T09:19:55Z`
- **Updated At**: `2026-06-01T14:08:43Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:parse_key_value`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1536)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

parse_key_value VRL function failed with the following real world linux auth log example:

```
parse_key_value!("TTY=unknown ; PWD=/ ; USER=postgres ; COMMAND=/usr/pgsql-10/bin/psql;", key_value_delimiter: "=", field_delimiter: ";")

```
I'm getting `could not parse whole line successfully` error

It is successfully parsed same string but with removed delimiter ";" at the end of string:

parse_key_value!("TTY=unknown ; PWD=/ ; USER=postgres ; COMMAND=/usr/pgsql-10/bin/psql", key_value_delimiter: "=", field_delimiter: ";")

### Configuration

```text

```

### Version

0.50

### Debug Output

```text

```

### Example Data

TTY=unknown ; PWD=/ ; USER=postgres ; COMMAND=/usr/pgsql-10/bin/psql;

### Additional Context

_No response_

### References

_No response_
