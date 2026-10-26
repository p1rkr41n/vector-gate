# [#1386] Add bitwise operators for integers

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1386)
- **Status**: `OPEN`
- **Author**: [@vruello](https://github.com/vruello)
- **Created At**: `2025-04-23T15:28:02Z`
- **Updated At**: `2026-06-01T14:19:27Z`
- **Comments**: 1
- **Labels**: `vrl:compiler`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1386)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

Logs often contain flags, which are integers where each bit has a special meaning. When processing a flag, it is useful to be able to know whether the n-th bit is set or not. The standard way to do this is to use a bitwise and operator.

### Attempted Solutions

I couldn't find any bitwise operators in the vrl language.

### Proposal

I suggest adding bitwise `and`, `or` and `not` operators for integers in the vrl language.

### References

_No response_
