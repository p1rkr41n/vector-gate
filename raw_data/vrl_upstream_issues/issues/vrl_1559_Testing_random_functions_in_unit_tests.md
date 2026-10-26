# [#1559] Testing random functions in unit tests

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1559)
- **Status**: `OPEN`
- **Author**: [@simplepad](https://github.com/simplepad)
- **Created At**: `2025-11-10T10:37:28Z`
- **Updated At**: `2026-06-01T14:19:42Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1559)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

Would be nice to be able to test `remap` transforms that use random functions like `uuid_v4()` and so on.

### Attempted Solutions

_No response_

### Proposal

Maybe add a way to specify a global seed to be used with every random function during tests? Could be a config option or a ENV variable.

### References

_No response_
