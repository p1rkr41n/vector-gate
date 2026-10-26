# Issue #962: Add timezone support for parse_timestamp

- **URL:** https://github.com/vectordotdev/vrl/issues/962
- **Author:** @sandervandegeijn
- **Status:** CLOSED (completed)
- **Created:** 2024-07-29T21:02:06Z
- **Closed:** 2025-01-06T15:51:18Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

I have a timestamp in localtime. Vector assumes it is UTC, offsetting the time with 2 hours (CEST currently, Europe/Amsterdam). Adding a timezone parameter can solve this.

### Attempted Solutions

Offsetting by hand, but we have summertime and wintertime...

### Proposal

Implement timezone parameter

### References

_No response_

### Version

0.39
