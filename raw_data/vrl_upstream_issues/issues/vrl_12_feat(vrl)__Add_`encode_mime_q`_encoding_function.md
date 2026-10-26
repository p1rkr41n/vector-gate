# [#12] feat(vrl): Add `encode_mime_q` encoding function

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/12)
- **Status**: `OPEN`
- **Author**: [@ktff](https://github.com/ktff)
- **Created At**: `2022-10-28T11:22:53Z`
- **Updated At**: `2026-06-01T14:17:26Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/12)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

A corresponding `decode_mime_q` function has been/will be added in https://github.com/vectordotdev/vector/pull/14813, and while usually decode/encode functions are both added in the same PR it is not clear how useful `encode_mime_q` encoding function would be. So it was decided to open this issue to gauge interest in it.

### Attempted Solutions

_No response_

### Proposal

Add vrl function `encode_mime_q` which would encode input string according to https://datatracker.ietf.org/doc/html/rfc2047. It would also accept arguments for desired encoding and charset.

### References

`decode_mime_q` - https://github.com/vectordotdev/vector/issues/14325

### Version

`v0.25.0`
