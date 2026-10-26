# [#28] `map_values` can infinitely recurse / stack overflow

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/28)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-09-08T16:11:43Z`
- **Updated At**: `2026-06-16T13:10:47Z`
- **Comments**: 1
- **Labels**: `vrl:compiler`, `stdlib:map_values`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/28)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

The following example has infinite recursion that overflows the stack.

```coffee
$ map_values({"a": {"b": true}}, recursive: true) -> |value|{{"c": {"d": true}}}
thread 'main' has overflowed its stack
fatal runtime error: stack overflow
Aborted (core dumped)
```


### Version

0.24.0

