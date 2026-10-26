# Issue #628: regex replace using a closure

- **URL:** https://github.com/vectordotdev/vrl/issues/628
- **Author:** @tmccombs
- **Status:** CLOSED (completed)
- **Created:** 2024-01-07T08:54:19Z
- **Closed:** 2024-01-24T03:39:26Z
- **Labels:** None

## Description

I filed https://github.com/vectordotdev/vrl/issues/633, but now realize that this might have been a better place to report it. 

For convenience I will copy over my text from there:

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


