# [#63] Cannot use empty blocks with VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/63)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2022-05-18T21:18:36Z`
- **Updated At**: `2026-06-01T14:05:32Z`
- **Comments**: 6
- **Labels**: `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/63)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

VRL doesn't seem to allow if conditions with empty blocks. One could argue that we maybe _shouldn't_ allow this (though I think we should), but, at the least, the error message could be much better than the one the lexer gives. The below yields:

```
error[E203]: syntax error
  ┌─ :3:1
  │
3 │ }
  │ ^
  │ │
  │ unexpected syntax token: "RBrace"
  │ expected one of: "\n", "!", "(", "[", "_", "abort", "false", "float literal", "function call", "identifier", "if", "integer literal", "null", "raw string literal", "regex literal", "string literal", "timestamp literal", "true", "{", "path literal"
  │
  = see language documentation at https://vrl.dev
```

### Configuration

```text
[sources.stdin]
type = "stdin"
decoding.codec = "json"

[transforms.remap]
type = "remap"
inputs = [ "stdin" ]
source = '''
.image = string(.image) ?? "unknown"
if starts_with(.image, "foo") {
}
'''

[sinks.my_sink_id]
type = "console"
inputs = [ "remap" ]
encoding.codec = "json"
```


### Version

vector 0.21.1

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
