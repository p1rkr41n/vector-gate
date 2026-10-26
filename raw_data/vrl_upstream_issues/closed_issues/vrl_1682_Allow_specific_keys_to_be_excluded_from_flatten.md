# Issue #1682: Allow specific keys to be excluded from `flatten`

- **URL:** https://github.com/vectordotdev/vrl/issues/1682
- **Author:** @benjamin-awd
- **Status:** CLOSED (completed)
- **Created:** 2026-03-04T17:07:15Z
- **Closed:** 2026-03-20T14:53:00Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

We often perform selective flattening for our payloads, meaning that we often need to exclude certain keys during the flattening operation. Currently this requires a somewhat verbose save/restore dance:

```coffee
metadata = del(.metadata)
tags = del(.tags)

. = compact(flatten(., "_"))

.metadata = metadata
.tags = tags
```

This is also useful for downstream consumers that do not necessarily want to flatten specific fields and instead want to store them within a JSON record/column.

### Attempted Solutions

_No response_

### Proposal

Add an optional `except` parameter to flatten that accepts an array of key names to exclude from flattening:

```coffee
. = compact(flatten(., "_", except: ["metadata", "tags"]))
```

Keys matching the except list would be preserved as-is while everything else is flattened normally.

### References

_No response_
