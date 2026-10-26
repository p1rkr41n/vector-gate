# [#42] Typedef for `merge` vrl function with deep = true is invalid

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/42)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-07-18T15:49:22Z`
- **Updated At**: `2026-06-16T13:10:52Z`
- **Comments**: 0
- **Labels**: `vrl:typedef`, `stdlib:merge`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/42)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

The type definition does not look at the `deep` parameter. It always assumes it's false.

```coffeescript
$ merge({"x": {"a": 1}},{"x": {"b": 2}}, false)
{ "x": { "b": 2 } }

$ type_def(merge({"x": {"a": 1}},{"x": {"b": 2}}, false))
{ "object": { "x": { "object": { "b": { "integer": true } } } } }

$ merge({"x": {"a": 1}},{"x": {"b": 2}}, true)
{ "x": { "a": 1, "b": 2 } }

$ type_def(merge({"x": {"a": 1}},{"x": {"b": 2}}, true))
{ "object": { "x": { "object": { "b": { "integer": true } } } } }
```

### Version

0.23.0

