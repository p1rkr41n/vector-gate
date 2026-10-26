# [#641] `parse_syslog` incorrectly adds the previous year for RFC3464 timestamps when close to the new year and the system timezone is not UTC

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/641)
- **Status**: `OPEN`
- **Author**: [@yangshike](https://github.com/yangshike)
- **Created At**: `2024-01-11T02:02:21Z`
- **Updated At**: `2026-06-16T13:10:11Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`, `stdlib:parse_syslog`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/641)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

When the system time is (+800) 2024-01-01 00:00:00 - 2024-01-01 08:00

The timestamp field parsed through parse_syslog becomes 2022, this bug  is reproducible

screenshot：

![image](https://github.com/vectordotdev/vector/assets/13585274/a6b72eb6-94a0-4cc3-89a4-6356bb92c075)
![image](https://github.com/vectordotdev/vector/assets/13585274/8582f280-f1cd-4522-be1e-69ffa5e629fc)


### Configuration

```text
[sources.message_log]
type = "file"
include = ["/var/log/messages"]
start_at_beginning = true
[transforms.modify_message_log]
type = "remap"
inputs = [ "message_log" ]
source = '''
. = parse_syslog!(.message)
'''
[sinks.console]
type = "console"
inputs = ["modify_message_log"]
encoding.codec = "json"
```


### Version

0.33

### Debug Output

_No response_

### Example Data

Comparison of original log and log processed by vector：
![image](https://github.com/vectordotdev/vector/assets/13585274/fc4df82e-b329-4bd5-9313-8712b5124ac5)


### Additional Context

_No response_

### References

_No response_
