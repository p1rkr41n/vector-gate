# [#35] VRL: Partially fallible blocks can create invalid type definitions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/35)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-08-01T19:54:35Z`
- **Updated At**: `2026-06-01T14:06:06Z`
- **Comments**: 2
- **Labels**: `vrl:typedef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/35)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

A block can contain fallible expressions, which propagates the fallibility up to the entire block. If the fallibility is handled there, that means that any fallible expression in the block can break execution out of the block, effectively making some of the expressions _optional_. The current type definition assumes all expressions will always execute. This can result in invalid type definitions.

Unfortunately, there is a diagnostic bug preventing an example reproducing this on `0.23.0` (https://github.com/vectordotdev/vrl/issues/36)

Below is an example reproducing the issue on `0.22.1`, but I believe this is also an issue in both `0.23.0` and master (once the above bug is fixed).

```coffeescript
$ type_def(.)
{ "object": {  }, "object_unknown_infinite": { "any": true } }

$ x, err = {.a=1;push(.x,1);.b=2}
"function call error for \"push\" at (15:25): expected array, got null"

$ .
{ "a": 1 }

$ type_def(.)
{ "object": { "a": { "integer": true }, "b": { "integer": true } } }
```

### Version

0.22.1

