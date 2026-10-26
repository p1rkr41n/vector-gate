# [#38] VRL: "success" value of fallible assignment expressions can have an invalid type def

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/38)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-07-29T19:21:20Z`
- **Updated At**: `2026-06-01T14:05:56Z`
- **Comments**: 0
- **Labels**: `vrl:typedef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/38)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

When a fallible function fails, the "success" variable is assigned a "default" value of the same type as if it actually succeeded. Unfortunately this value is simplified and doesn't always necessarily match the type definition. Fixing the return value to actually match the type definition is _impossible_ in the general case, therefore the type definition must change. Making the type definition match the current return value might be problematic and will make using the returned value more difficult though.


```coffeescript
$ x, err = push(.x, 1)
"function call error for \"push\" at (9:20): expected array, got null"

$ type_def(x)
{ "array": { "0": { "integer": true } }, "array_unknown_infinite": { "any": true } }

$ type_def(x[0])
{ "integer": true }

$ x[0]
null
```


A solution to this might also address https://github.com/vectordotdev/vrl/issues/74


### Version

0.23.0
