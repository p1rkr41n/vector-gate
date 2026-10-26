# [#52] Add type_def checking to existing VRL tests

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/52)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-06-16T16:46:38Z`
- **Updated At**: `2026-06-16T13:10:57Z`
- **Comments**: 2
- **Labels**: `vrl:typedef`, `stdlib:type_def`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/52)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Proposal

Vector currently doesn't have anything checking the type definitions of functions against the actual values that can be returned. Type checking should be added to our existing testing suite. For any value returned, it can be checked against the type-def to make sure it is valid. This can't check every type-def issue, but it should catch many of them.

