# Issue #197: Closures are compiled assuming they only run exactly once

- **URL:** https://github.com/vectordotdev/vrl/issues/197
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2022-08-01T15:20:42Z
- **Closed:** 2026-05-01T19:13:01Z
- **Labels:** vrl:compiler, vrl:typedef

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Closures can be ran any number of times, including none. But type definitions are calculated assuming they run exactly once, which can result in invalid type definitions.

### Example
```coffeescript
$ . = {}
{  }

$ map_values([]) -> |i| {.a = "foo"}
[]

$ type_def(.)
{ "object": { "a": { "bytes": true } } }

$ .
{  }
```


### Version

0.23.0

