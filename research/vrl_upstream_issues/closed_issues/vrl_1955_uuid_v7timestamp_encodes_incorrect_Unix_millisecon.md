# Issue #1955: `uuid_v7(timestamp)` encodes incorrect Unix milliseconds

- **URL:** https://github.com/vectordotdev/vrl/issues/1955
- **Author:** @abbit
- **Status:** CLOSED (completed)
- **Created:** 2026-09-19T09:52:15Z
- **Closed:** 2026-09-21T14:11:19Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

`uuid_v7(timestamp)` does not correctly encode the input timestamp in the UUIDv7 timestamp field.

UUIDv7 stores Unix milliseconds in its first 48 bits. For `2026-01-01T00:00:00.123456789Z`, the UUID should start with `019b76da-a87b-7`, but the generated UUID has a different timestamp prefix.

The input timestamp should be preserved with millisecond precision.

### VRL Program

```text
id = uuid_v7(t'2026-01-01T00:00:00.123456789Z')
prefix = replace(slice!(string!(id), 0, 13), "-", "")
assert_eq!(prefix, "019b76daa87b")
```

### VRL and/or Vector Version

VRL 0.35.0 (current upstream main)

### Debug Output

```text

```

### Example

_No response_

### Additional Context

_No response_

### References

_No response_
