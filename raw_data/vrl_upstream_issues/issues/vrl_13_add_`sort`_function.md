# [#13] add `sort` function

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/13)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-10-13T14:40:59Z`
- **Updated At**: `2026-06-01T14:17:24Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/13)

---

## Description

<!--
Hi there,

Thank you for opening an issue. Please note that we try to keep the Vector issue tracker reserved for bug reports and feature requests. For general usage questions, please see: https://chat.vector.dev.
-->

<!--- Please keep this note for the community --->

### Community Note

* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment

<!--- Thank you for keeping this note for the community --->

### Use-cases

It's useful to be able to sort arrays. This is currently possible using `for_each` and a manual implementation, but it's less performant and more cumbersome to do than with a dedicated `sort` function.

We could also add a `sort_by` function later, that works similar to `sort`, except that it takes a closure and returns -1/0/1 to determine if a value should be sorted before/after the other value.
