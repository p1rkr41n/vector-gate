# Issue #1903: to_syslog_severity should also accept "critical" instead of just "crit"

- **URL:** https://github.com/vectordotdev/vrl/issues/1903
- **Author:** @ypid-work
- **Status:** CLOSED (completed)
- **Created:** 2026-08-26T12:09:02Z
- **Closed:** 2026-10-22T19:36:34Z
- **Labels:** stdlib:to_syslog_severity

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->

### Problem

Every other long and short variant is accepted. Only "critical" is not:

https://github.com/vectordotdev/vrl/blob/eae43fef51bbe122a87281b5edfae5e03fe8d168/src/stdlib/to_syslog_severity.rs#L7-L14

This is inconsistent. Many logs output "critical".  

### VRL Program

```text
$ to_syslog_severity!("critical")
function call error for "to_syslog_severity" at (0:31): syslog level critical not valid
```

### VRL and/or Vector Version

main of vrl (eae43fef51bbe122a87281b5edfae5e03fe8d168)

### Debug Output

```text

```

### Example

_No response_

### Additional Context

_No response_

### References

It was like this since the function to_syslog_severity was added in 2020 with https://github.com/vectordotdev/vector/pull/5505/changes#diff-c5ded71d379021035f4d1b0db4523d091cd12c4acc4e3b5129cb555bebd3277bR41

The codec already supports "critical" with https://github.com/vectordotdev/vector/pull/25731
