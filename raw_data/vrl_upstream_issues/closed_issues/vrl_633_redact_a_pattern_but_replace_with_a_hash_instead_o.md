# Issue #633: redact a pattern, but replace with a hash instead of  a string

- **URL:** https://github.com/vectordotdev/vrl/issues/633
- **Author:** @tmccombs
- **Status:** CLOSED (completed)
- **Created:** 2024-01-06T04:29:49Z
- **Closed:** 2024-02-06T17:02:05Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

I want to redact certain personally identifiable information, such as an email address, from logs, but in such a way that if I already know the information (email address), I can search the logs for matching log entries. 



### Attempted Solutions

I think it would be possible to do this with a lua transform. But  the documentation for that says to create an issue if the remap transform doesn't meet my needs.

Lua also doesn't have a built in sha256 function so I would either need to use a lua native sha256 implementation, which I suspect would be slow, or pull in a shared library that adds such a function for lua (is that possible with vector?)

### Proposal

I can think of a few ways this could be done:

- Add an option to the redact function that will replace the matched string with a hash of itself, Possibly with a configurable hash function, instead of with a fixed string.
- add a new function  that replaces a matching regex with its hash
- make a function like replace, but instead of a string for the replacement, it uses a closure to compute a replacement value.

I think that the last bullet point is the most general and could be useful in other cases as well. 

P.s. having a built in redaction pattern for email addresses would be awesome.

### References

_No response_

### Version

_No response_
