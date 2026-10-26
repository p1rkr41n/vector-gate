# [#62] `logfmt` does not conform to spec

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/62)
- **Status**: `OPEN`
- **Author**: [@jalaziz](https://github.com/jalaziz)
- **Created At**: `2022-05-19T08:32:51Z`
- **Updated At**: `2026-06-01T14:05:34Z`
- **Comments**: 8
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/62)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Even with vectordotdev/vector#12700, Vector's `logfmt` encoding does not conform to the semi-official [logfmt spec](https://pkg.go.dev/github.com/kr/logfmt).

In particular, the handling of quoted keys and values is still off. Some example scenarios are:
1. Keys that include whitespace, equal signs, and quotes. These are all technically invalid according to the spec. The [go-logfmt](https://pkg.go.dev/github.com/go-logfmt/logfmt) library seems to handle this by removing the invalid characters.
2. Quoted keys. Related to #1. Keys should never be quoted.
3. Values containing equal signs. These values should be quoted.

### Configuration

```toml
[sources.in]
type = "stdin"

[transforms.modify]
type = "remap"
inputs = ["in"]
source = '''
  . = parse_json!(.message)
  . = encode_logfmt(.)
'''

[sinks.out]
inputs = ["modify"]
type = "console"
encoding.codec = "text"
```


### Version

0.22

### Debug Output

_No response_

### Example Data
```json
{"test key": "test value", "test=key": "test=value", "test\"key": "test\"value"}
```
### Additional Context

I've put together some basic tests of [go-logfmt](https://pkg.go.dev/github.com/go-logfmt/logfmt) in this [Go playground](https://go.dev/play/p/T7D6jV7drfQ).

The current implementation of `logfmt` in Vector relies on `encode_key_value`. Despite `logfmt` being the primary use case for `encode_key_value`, fixing these issues seems `logfmt`-specific. One option might be preprocessing keys and values to match the spec?

Additionally, even though `go-logfmt` drops invalid characters from keys, other options may be more desirable (e.g. replacing invalid characters with underscores).

### References

vectordotdev/vector#12674
