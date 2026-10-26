# [#40] chore(vrl): Improve `Kind::canonicalize`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/40)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-07-25T16:43:59Z`
- **Updated At**: `2023-03-28T13:21:22Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:typedef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/40)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

A simple implementation of `Kind::canonicalize` was added in https://github.com/vectordotdev/vector/pull/13619. This is mostly useful in tests and during debugging since `Kind` can have multiple internal representations that are equivalent. When refactoring a function that returns a `Kind`, it might return a "correct" result but it could be a different representation than is being asserted in tests.

The `Kind::canonicalize` function currently does some of the easy simplification such as removing `known` fields that exactly match the `unknown` type. There are more things that can be simplified, such as the `unknown` type. Also add better documentation for what the "simplified" representation is.

