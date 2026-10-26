# [#57] VRL: `parse_logfmt` seems to actually be infallible

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/57)
- **Status**: `OPEN`
- **Author**: [@spencergilbert](https://github.com/spencergilbert)
- **Created At**: `2022-06-03T19:14:30Z`
- **Updated At**: `2026-06-16T13:11:02Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:parse_logfmt`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/57)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Provided the `value` passed to `parse_logfmt` is a String, I'm not sure the parsing can ever fail.

Example:
```coffee
$ parse_logfmt!("foobar baz=1 bizz = bar:// asdklfjhaklsjd n aksjdhfj jaj  ")
{ "aksjdhfj": true, "asdklfjhaklsjd": true, "baz": "1", "bizz": "bar://", "foobar": true, "jaj": true, "n": true }
```

Based on the referenced issue, our infallible parsing may be due to an implementation issue of the "spec".

If that's the case and a better implementation allows parsing to be fallible we should do so, otherwise the function should be marked as infallible.

### Configuration

_No response_

### Version

vector 0.22.0 (x86_64-apple-darwin 5e937e3 2022-06-01)

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

https://github.com/vectordotdev/vrl/issues/62
