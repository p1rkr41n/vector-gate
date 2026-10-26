# [#74] Merging via `|=` for fallible functions resets the left hand side when there is an error

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/74)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2022-03-11T16:27:03Z`
- **Updated At**: `2026-06-01T14:05:18Z`
- **Comments**: 2
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/74)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

It seems like, when using `|=` with a return value from a fallible function, if an error occurs, the value assignment doesn't merge, but assigns instead to `{}`.

### Configuration

```text
$ . = {"message": "foo"}
{ "message": "foo" }

$ ., err |= parse_syslog(.no_exist)
"function call error for \"parse_syslog\" at (10:33): expected \"string\", got \"null\""

$ .
{  }
```


### Version

vector 0.20.0 (x86_64-apple-darwin 2a706a3 2022-02-10)

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
