# [#823] from_unix_timestamp float support

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/823)
- **Status**: `OPEN`
- **Author**: [@jpds](https://github.com/jpds)
- **Created At**: `2024-05-06T09:38:04Z`
- **Updated At**: `2026-06-16T13:10:02Z`
- **Comments**: 2
- **Labels**: `vrl:stdlib`, `stdlib:from_unix_timestamp`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/823)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Caddy logs timestamps as floats: `"ts":1714987958.264331` - however the `from_unix_timestamp` only takes integers.

### Attempted Solutions

I've worked around this by calling `to_int!(.ts)`, however it'd be nice to keep the sub-second accuracy for request order sorting.

### Proposal

_No response_

### References

_No response_

### Version

0.37.1
