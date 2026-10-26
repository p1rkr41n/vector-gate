# [#1558] Add `ord` and `chr` functions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1558)
- **Status**: `OPEN`
- **Author**: [@simplepad](https://github.com/simplepad)
- **Created At**: `2025-11-10T08:48:42Z`
- **Updated At**: `2026-06-01T14:19:41Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1558)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

My particular use case is checking bit flags in a string of raw bytes. When https://github.com/vectordotdev/vrl/issues/1386 lands, it will add the required comparison functions, but I also need a way to convert a raw byte (a string) into an integer.

### Attempted Solutions

_No response_

### Proposal

Add two functions:
1. `ord(value: string, [position: integer])` - gives integer representation of the first character in a string (optionally the character at a certain position), this is a workaround for VRL not having a character type.
2. `chr(value: integer)` - converts an integer into a character, the inverse of `ord()`

These functions should probably be added to the "Convert functions" section.

### References

_No response_
