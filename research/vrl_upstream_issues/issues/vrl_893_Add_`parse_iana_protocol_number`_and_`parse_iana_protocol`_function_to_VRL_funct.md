# [#893] Add `parse_iana_protocol_number` and `parse_iana_protocol` function to VRL functions.

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/893)
- **Status**: `OPEN`
- **Author**: [@AlexYangYu](https://github.com/AlexYangYu)
- **Created At**: `2024-04-06T03:16:26Z`
- **Updated At**: `2026-06-01T14:18:30Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/893)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

In scenarios that parsing network device logs, it is necessary to translate the protocol number in the logs into protocol, a conversion that should be done in accordance with the [IANA Protocol Number ](https://www.iana.org/assignments/protocol-numbers/protocol-numbers.xhtml) standards.

For example: 
- `1` - > ` ICMP`
- `6` -> `TCP`

### Attempted Solutions

Currently, I only have two choice:
- handle number and protocol mapping at app later;
- wirte long sentence of `if` and `else` in remap transform, because I can not found vrl support map struct.

### Proposal

add function in vrl for parsing the protocol num and protocol

### References

_No response_

### Version

_No response_
