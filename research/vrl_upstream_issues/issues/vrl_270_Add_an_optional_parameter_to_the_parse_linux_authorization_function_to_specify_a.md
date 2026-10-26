# [#270] Add an optional parameter to the parse_linux_authorization function to specify a timezone

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/270)
- **Status**: `OPEN`
- **Author**: [@Qazeer](https://github.com/Qazeer)
- **Created At**: `2022-09-21T10:15:25Z`
- **Updated At**: `2026-06-16T13:10:42Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`, `stdlib:parse_linux_authorization`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/270)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

The VRL `parse_linux_authorization` function uses the timezone of the current machine (the one executing Vector) to convert timestamps to UTC. The timezone of the current machine may differ from the timezone of the original machine (that emitted the logs), thus potentially creating a disparity between the deduced and original timestamps.



### Attempted Solutions

Within Vector's existing features, a timestamp could be converted to a string with `format_timestamp`, the timezone manually added, and the timestamp string converted back to a timestamp using `to_timestamp`.  But this solution is quite hacky.

### Proposal

A better solution would be to add an optional parameter for the `parse_linux_authorization` function to specify the timezone of the log files and use the specified timezone for the conversion to UTC directly within `parse_linux_authorization`.

### References

_No response_

### Version

vector 0.24.0 (x86_64-pc-windows-msvc 43267b9 2022-08-30)
