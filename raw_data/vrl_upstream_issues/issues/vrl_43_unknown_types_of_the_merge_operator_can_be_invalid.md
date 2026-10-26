# [#43] unknown types of the merge operator can be invalid

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/43)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-07-15T16:21:37Z`
- **Updated At**: `2026-06-01T14:05:49Z`
- **Comments**: 0
- **Labels**: `vrl:typedef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/43)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I haven't worked out an easy example to reproduce this yet, mostly just writing this one down before I forget.

When merging 2 objects with the merge operator (`|` or `|=`), the unknown is merged together with "overwrite" still enabled. This means that the type assumes the right-side argument will always overwrite all left-side unknown fields. This isn't true, and should probably merge the unknown with "union" instead.

### Version

0.23.0
