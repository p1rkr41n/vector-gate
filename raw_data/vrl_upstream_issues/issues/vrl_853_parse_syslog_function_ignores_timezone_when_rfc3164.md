# [#853] parse_syslog function ignores timezone when rfc3164

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/853)
- **Status**: `OPEN`
- **Author**: [@timansky](https://github.com/timansky)
- **Created At**: `2024-05-19T01:06:36Z`
- **Updated At**: `2026-06-16T13:09:59Z`
- **Comments**: 3
- **Labels**: `vrl:stdlib`, `stdlib:parse_syslog`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/853)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->

### Problem

Most devices are sending logs in [rfc3164](https://blog.datalust.co/seq-input-syslog/#rfc3164) format, which does not contain timezone.
When syslog message in rfc3164 format, parse_syslog function always using UTC [timezone](https://vector.dev/docs/reference/configuration/transforms/remap/#timezone) when parsing timestamp

### Configuration

```text
transform:
  adapt_syslog:
    type: remap
    timezone: "Asia/Almaty" # Apply this timezone when parsing timestamp
    inputs:
    - syslog
    source:  |
      d = parse_timestamp!("May 19 2024 12:00:00", format: "%h %d %Y %T")
      log("debug1:" + format_timestamp!(d, format: "%+"))

      d = parse_syslog!(s'<180>May 19 2024 12:00:00 hostname message')
      log("debug2:" + format_timestamp!(d.timestamp, format: "%+"))
```


### Version

 0.38.0

### Debug Output

```text
INFO transform{component_kind="transform" component_id=adapt_syslog component_type=remap}: vrl::stdlib::log: Internal log [debug1:2024-05-19T07:00:00+00:00] is being suppressed to avoid flooding.

INFO transform{component_kind="transform" component_id=adapt_syslog component_type=remap}: vrl::stdlib::log: Internal log [debug2:2024-05-19T12:00:00+00:00] is being suppressed to avoid flooding.
```


### Example Data

<180>May 19 2024 12:12:12 hostname message

### Additional Context

_No response_

### References

_No response_
