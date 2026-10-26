# Issue #848: New Remap function for parse_syslog_facility

- **URL:** https://github.com/vectordotdev/vrl/issues/848
- **Author:** @timansky
- **Status:** CLOSED (completed)
- **Created:** 2024-05-17T13:01:46Z
- **Closed:** 2025-01-27T16:21:51Z
- **Labels:** vrl:stdlib, good first issue

## Description

### A note for the community
<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->

Similar to request to map syslog severity levels to integer from https://github.com/vectordotdev/vector/issues/5501 it would be helpful to have a means to remap [syslog facility keywords](https://en.wikipedia.org/wiki/Syslog#Facility) to their integer values as well.

### Use Cases

When parsing events message, the raw facility values could be enriched with a simple remap transform to down stream processing

### Attempted Solutions

_No response_

### Proposal

create a remap-function to_syslog_facility which could produce the facility name:

parse_syslog_facility("authpriv")
=> 10

### References

_No response_

### Version

_No response_
