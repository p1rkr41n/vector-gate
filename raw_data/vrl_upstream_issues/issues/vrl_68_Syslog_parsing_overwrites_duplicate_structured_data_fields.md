# [#68] Syslog parsing overwrites duplicate structured data fields

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/68)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2022-04-27T19:24:16Z`
- **Updated At**: `2026-06-01T14:05:29Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/68)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Noticed by https://github.com/vectordotdev/vector/pull/12433#discussion_r860138956

[RFC5424](https://datatracker.ietf.org/doc/html/rfc5424#section-6.3.3) allows for keys to be repeated in structured data elements. Currently, Vector assumes the keys are unique and so you will only end up with one of the values in the resulting parsed object.

For repeated keys, the value should be an array of all values seen.

### Configuration

_No response_

### Version

Vector 0.21.1

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

* https://github.com/vectordotdev/vector/pull/12433
* https://github.com/vectordotdev/vector/issues/12431
* https://github.com/vectordotdev/vector/issues/12410#issuecomment-1111158213
