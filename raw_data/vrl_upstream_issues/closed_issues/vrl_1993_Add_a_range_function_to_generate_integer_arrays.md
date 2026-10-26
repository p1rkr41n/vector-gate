# Issue #1993: Add a `range` function to generate integer arrays

- **URL:** https://github.com/vectordotdev/vrl/issues/1993
- **Author:** @lchabert
- **Status:** CLOSED (completed)
- **Created:** 2026-10-14T06:28:48Z
- **Closed:** 2026-10-23T20:24:39Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->

### Use Cases

Some inputs encode integer sets as compact ranges, for example `"500..512"` or `"1-4094"`. Expanding them into the list of integers is not possible in VRL today.

### Attempted Solutions

VRL has no way to create an array of N integers (`range(1, 4)` returns error E105, undefined function), and `for_each` only iterates over a collection that already exists. The only workaround we found is to embed a literal array of all possible values and `slice` it.

### Proposal

Add a `range` function to the stdlib, similar to Python's `range`:

```coffee
range(start: integer, end: integer, [step: integer = 1]) :: array, fallible
```

- Half-open: `range(500, 513)` returns `[500, 501, ..., 512]`.
- `step` can be negative: `range(5, 0, -1)` returns `[5, 4, 3, 2, 1]`.
- It errors if `step == 0`, and if the result would exceed a size limit, to protect against memory exhaustion. The limit is open for discussion: a fixed maximum, or an optional argument.
- An empty range returns `[]`.

Example:

```coffee
bounds = split(string!(.ids), "..")
.ids = range!(to_int!(bounds[0]), to_int!(bounds[1]) + 1)
```

We would be happy to submit a PR for this.

### References

- #1297 (`break` in iterations): related, since iteration in VRL is limited to existing collections.

