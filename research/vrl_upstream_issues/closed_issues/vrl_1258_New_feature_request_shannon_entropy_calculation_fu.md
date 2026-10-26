# Issue #1258: New feature request: shannon entropy calculation function

- **URL:** https://github.com/vectordotdev/vrl/issues/1258
- **Author:** @johnhtodd
- **Status:** CLOSED (completed)
- **Created:** 2025-02-07T18:43:26Z
- **Closed:** 2025-02-14T17:50:04Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

We sometimes need to detect if names are random or non-random in nature (mostly DNS in nature, but sometimes useful for other string types.)  This triggers various additional analysis or enrichment.

### Attempted Solutions

There is really no way to do this via other methods unless done offboard.

### Proposal

There are existing Rust libraries for determining Shannon entropy.  This would be a function that is fairly simple - a string is provided, and a numeric result is provided. 

https://crates.io/crates/shannon-entropy

I could imagine this as a function that falls into the "string functions" category.   Something like:

```
  shannon_entropy(value: <string> )
    :: integer
```


### References

_No response_

### Version

n/a
