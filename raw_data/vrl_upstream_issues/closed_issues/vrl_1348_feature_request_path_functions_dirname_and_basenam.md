# Issue #1348: [feature request] path functions dirname and basename

- **URL:** https://github.com/vectordotdev/vrl/issues/1348
- **Author:** @shantanugadgil
- **Status:** CLOSED (completed)
- **Created:** 2025-03-18T05:31:43Z
- **Closed:** 2025-10-06T18:39:06Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->

Based on the discussion at: 
https://github.com/vectordotdev/vector/discussions/22657

### Use Cases

Based on the discussion at https://github.com/vectordotdev/vector/discussions/22657 I want to be able to extract the "name only" part of a filename_with_extension. I want to use that extracted "only name" as a "service label" when forwarding the logs to Loki.

Hence I am requesting the path functions like dirname and basename

### Attempted Solutions

The attempted solution is already at: 
https://github.com/vectordotdev/vector/discussions/22657

### Proposal

In addition to the simple `basename`/`dirname` functions, if there was a function to directly yield the "only file name" part, it could be even-more-awesome! 🙂 

### References

_No response_
