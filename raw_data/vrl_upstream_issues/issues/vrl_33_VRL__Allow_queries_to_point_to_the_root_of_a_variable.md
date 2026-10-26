# [#33] VRL: Allow queries to point to the root of a variable

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/33)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-08-10T17:29:57Z`
- **Updated At**: `2023-03-28T13:18:05Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/33)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Currently functions that take "query" arguments cannot point to the root of a local variable. It might be useful to allow this.

That means you can't call the following functions with arguments pointing to the root of a local variable
- `del`
- `exists`
- `unnest`

While `del` and `exist` might not be particularly useful on the root of a local variable, it could be reasonable to use `unnest`, or some future function that uses queries. And from a consistency perspective, it would be nice to support it.
You can today, for example, call `unnest` on the root event, or event `del` the root event, but not a local variable.


### Version

master / 1b5f585e7b213ca3fd370ba6a7462572207b6e4c
