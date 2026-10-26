# Issue #269: Add `lossy` option to `parse_json` function

- **URL:** https://github.com/vectordotdev/vrl/issues/269
- **Author:** @jszwedko
- **Status:** CLOSED (completed)
- **Created:** 2023-02-21T13:40:37Z
- **Closed:** 2024-08-15T18:41:36Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Users want to decode incoming bytes as JSON even if they contain invalid UTF-8 data in VRL.

### Attempted Solutions

Not currently possible.

### Proposal

Add an optional `lossy` parameter to `parse_json`. Default this to `true` since we expect this to be the most commonly desired behavior.

### References

- https://github.com/vectordotdev/vector/pull/16324
- https://github.com/vectordotdev/vector/issues/11577
- https://github.com/vectordotdev/vector/issues/10571
- https://github.com/vectordotdev/vector/issues/16406

### Version

vector 0.27.0
