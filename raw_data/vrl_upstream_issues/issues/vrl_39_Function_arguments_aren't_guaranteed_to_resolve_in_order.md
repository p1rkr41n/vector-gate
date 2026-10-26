# [#39] Function arguments aren't guaranteed to resolve in order

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/39)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-07-28T19:33:33Z`
- **Updated At**: `2026-06-01T14:05:54Z`
- **Comments**: 1
- **Labels**: `vrl:compiler`, `vrl:typedef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/39)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

When calculating the type definition of a function call, the arguments are evaluated in order, from left to right.

However, there is nothing that guarantees the actual arguments are resolved in the same order (or resolved at all).

Arguments should be resolved in order and only the `Value` passed to functions.

```coffeescript

$ format_number(1000, 2, {.foo = "message"; "."}, {.foo = true; ","})
"1,000.00"

$ .
{ "foo": "message" }

$ type_def(.)
{ "object": { "foo": { "boolean": true } } }
```

### Version

master / 9a049b5d18590a195aec0fa8958f80245ca1c3b0

