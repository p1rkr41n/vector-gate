# [#73] `parse_grok` VRL function ignores nonmatching characters at the start of the string, `parse_groks` errors

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/73)
- **Status**: `OPEN`
- **Author**: [@StephenWakely](https://github.com/StephenWakely)
- **Created At**: `2022-03-30T20:31:04Z`
- **Updated At**: `2026-06-16T13:11:11Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:parse_grok`, `stdlib:parse_groks`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/73)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

With `parse_grok`:

```
$ parse_grok!("nork32", "%{NUMBER: num}")
{ "num": 32 }
```

With `parse_groks`:

```
$ parse_groks!( "nork32", ["%{NUMBER: num}"])
function call error for "parse_groks" at (0:43): unable to parse grok: value does not match any rule
```

Both functions should behave the same here.

### Configuration

_No response_

### Version

v0.20

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
