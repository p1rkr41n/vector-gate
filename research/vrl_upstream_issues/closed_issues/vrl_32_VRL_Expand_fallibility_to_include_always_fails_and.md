# Issue #32: VRL: Expand fallibility to include "always fails", and generate a compile time error when this happens

- **URL:** https://github.com/vectordotdev/vrl/issues/32
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2022-08-12T23:35:24Z
- **Closed:** 2023-11-09T15:19:13Z
- **Labels:** vrl:compiler

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Today the concept of fallibility is a boolean. It can either fail, or not fail. It might be useful to expand this to 3 options:
- can't fail
- might fail
- always fails

And in the case where it always fails, a compile time error (or warning) might be useful. Even if this isn't used to generate compile time errors, it can be useful in the future for performance optimizations.

For example, consider the following code. The "start" parameter is known at compile time to always be invalid, but it still compiles.
```coffeescript
slice!("", 1)
```

### Version

0.23.0
