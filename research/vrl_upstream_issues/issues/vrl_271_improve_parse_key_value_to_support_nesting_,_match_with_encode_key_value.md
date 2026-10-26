# [#271] improve parse_key_value to support nesting , match with encode_key_value

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/271)
- **Status**: `OPEN`
- **Author**: [@ccmsi](https://github.com/ccmsi)
- **Created At**: `2022-09-05T11:32:50Z`
- **Updated At**: `2026-06-16T13:10:50Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:parse_key_value`, `stdlib:encode_key_value`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/271)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Goals:
 - make parse_key_value able to interpreted nested / structured data
 - make parse_key_value match encode_key_value

Currently:
```coffee
parse_key_value!(encode_key_value({"agent": {"name": "vector"}, "log": {"file": {"path": "my.log"}}, "event": "log"}))
{ "agent.name": "vector", "event": "log", "log.file.path": "my.log" }
```

Request:
```coffee
parse_key_value!(encode_key_value({"agent": {"name": "vector"}, "log": {"file": {"path": "my.log"}}, "event": "log"}), nesting: true)
{"agent": {"name": "vector"}, "log": {"file": {"path": "my.log"}}, "event": "log"}
```

This change allows parse_key_value to support parse regex such that parse_regex output in VRL can be made equivalent to old parse_regex transform parsing into nested data in an easy way.

```coffee
.fromregex = {"x.x":1, "x.y":2}
parse_key_value!(encode_key_value(.fromregex), nesting: true)
{'x': {'x':1, 'y':2}}
```

### Attempted Solutions

Found no way to translate dotted field names into nested/ structured object.

### Proposal

_No response_

### References

_No response_

### Version

_No response_
