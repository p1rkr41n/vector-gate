# [#21836] Implement VRL encoder

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/21836)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2024-11-19T21:04:53Z`
- **Updated At**: `2026-02-23T14:38:54Z`
- **Comments**: 0
- **Labels**: `domain:codecs`, `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/21836)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

We already have a VRL decoder. This ticket is to track the other part of the work i.e. the VRL encoder. 

Config snippet:
```
encoding.codec = "vrl"
encoding.source = '''
    encode_json(.) ?? encode_key_value!(.)
```

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

https://github.com/vectordotdev/vector/issues/13634

### Version

_No response_
