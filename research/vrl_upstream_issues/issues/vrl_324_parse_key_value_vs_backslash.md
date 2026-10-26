# [#324] parse_key_value vs backslash

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/324)
- **Status**: `OPEN`
- **Author**: [@grinapo](https://github.com/grinapo)
- **Created At**: `2023-07-13T17:11:27Z`
- **Updated At**: `2026-06-16T13:10:27Z`
- **Comments**: 7
- **Labels**: `vrl:stdlib`, `meta:confirmed`, `stdlib:parse_key_value`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/324)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

It seems `parse_key_value` gets confused when the first character of the string is `\\`

```
vector vrl
$ a="foo=11 T=\"p\\ip pap pop\""
$ b="foo=11 T=\"\\ip pap pop\""
$ a
"foo=11 T=\"p\\ip pap pop\""

$ b
"foo=11 T=\"\\ip pap pop\""

$ parse_key_value!(a)
{ "T": "p\\ip pap pop", "foo": "11" }

$ parse_key_value!(b)
{ "T": "\"\\ip", "foo": "11", "pap": true, "pop"": true }
```


### Configuration

_No response_

### Version

vector 0.30.0 (x86_64-unknown-linux-gnu 38c3f0b 2023-05-22 17:38:48.655488673)

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_

Hmm, maybe this issue shall be moved under https://github.com/vectordotdev/vrl - I am not yet familar about how you prefer collecting issues.
