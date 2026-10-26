# [#48] Improve typedef of `del` when deleting object fields

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/48)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-07-12T17:57:48Z`
- **Updated At**: `2026-06-16T13:10:54Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:typedef`, `stdlib:del`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/48)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Right now `del` removes the type definition of the value that is deleted. This is correct when the type is "closed" (no unknown values), however if the type has an unknown of "any", which is the most common value, then removing the type definition during `del` causes the type of the deleted value to be `any` even though it is known that is cannot exist. The closest type we could set it to today is `null` (since that's what accessing the deleted value will actually return). I think it's time to introduce the `undefined` type though, and set that instead.

CLI Playground example
```text
$ .x = 5
5

$ type_def(.x)
{ "integer": true }

$ del(.x)
5

$ .x
null

$ type_def(.x)
{ "any": true }

```

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

_No response_

### Version

0.23.0
