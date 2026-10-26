# Issue #970: include camelCase in VRL

- **URL:** https://github.com/vectordotdev/vrl/issues/970
- **Author:** @leshow
- **Status:** CLOSED (completed)
- **Created:** 2024-08-01T19:51:51Z
- **Closed:** 2024-08-07T18:25:04Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

a common operation is translating keys between snake_case, camelCase, PascalCase, etc. It would be nice to have this supported directly in VRL along with existing `downcase` and `upcase` functions.

### Attempted Solutions

Some manual VRL script is the only other option

### Proposal

Have not looked into the implementation details but I would propose adding those API functions which do the transformation. I'm happy to attempt a PR if someone can point me to a good place to start.

### References

_No response_

### Version

0.40.0
