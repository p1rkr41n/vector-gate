# [#27] `map_values` function closure argument type def can be invalid when using `recursive: true`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/27)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-09-08T16:22:41Z`
- **Updated At**: `2026-06-16T13:10:45Z`
- **Comments**: 0
- **Labels**: `vrl:typedef`, `stdlib:map_values`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/27)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

If you run the following line
```coffee
map_values({"a": "string", "b": {"c": 3}}, recursive: true) -> |value|{log(type_def(value))}
```
The output shows the type definition of `value`, which is
```json
{"bytes":true,"object":{"c":{"integer":true}}}
```
Since `recursive` is true, this should have included an `integer` (at the root), but it doesn't.

The following example shows that the integer is indeed passed into the closure, which aborts if ran.
```coffee
map_values({"a": "string", "b": {"c": 3}}, recursive: true) -> |value|{if is_integer(value) {abort} else {value
```


The issue is even worse if you modify the input as it's running, and the modifications add types that didn't originally exist.
This may not have been intentional though, and it covered under this issue instead: https://github.com/vectordotdev/vrl/issues/28


### Version

0.24.0


