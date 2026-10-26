# [#53] Add `zip` function to VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/53)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2022-06-10T21:20:38Z`
- **Updated At**: `2026-06-16T13:10:59Z`
- **Comments**: 6
- **Labels**: `vrl:stdlib`, `stdlib:zip`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/53)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

While writing up upgrade docs from the old `tokenizer` transform to `remap`, I realized it'd be helpful to have a `zip` function in VRL that would take two arrays, one of keys, one of fields, and create an object.

### Attempted Solutions

_No response_

### Proposal

```
$ zip(["a", "b"], [1, 2])

{ "a": 1, "b": 2}
```

Will have to decide on what should happen when the arrays don't match in length.

### References

_No response_

### Version

vector 0.22.0
