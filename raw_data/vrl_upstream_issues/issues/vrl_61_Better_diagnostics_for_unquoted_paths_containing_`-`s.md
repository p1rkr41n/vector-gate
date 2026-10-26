# [#61] Better diagnostics for unquoted paths containing `-`s

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/61)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2022-05-24T16:33:06Z`
- **Updated At**: `2026-06-01T14:16:48Z`
- **Comments**: 4
- **Labels**: `vrl:diagnostic`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/61)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Users are frequently tripped up by trying to use paths in VRL that contain a `-`.

These currently output errors like:

```
May 24 15:03:31 brannan11 vector[12970]: 1 │ .instance_id = del!(.instance-id)
May 24 15:03:31 brannan11 vector[12970]:   │                               ^^
May 24 15:03:31 brannan11 vector[12970]:   │                               │
May 24 15:03:31 brannan11 vector[12970]:   │                               undefined variable
May 24 15:03:31 brannan11 vector[12970]:   │                               did you mean "null"?
```

(example from https://github.com/vectordotdev/vector/issues/12839)

### Attempted Solutions

_No response_

### Proposal

I think the compiler could be enhanced to look for this common case of neglecting to quote a path containing a `-` by looking for expressions with `-` where the RHS is an undefined variable. Additionally, the lack of spaces around the `-` could be an indicator. When this is observed, the diagnostics could suggest to the user that maybe they meant to quote the expression to use it as a path.

### References

* https://github.com/vectordotdev/vector/issues/12839

### Version

vector v0.21.2
