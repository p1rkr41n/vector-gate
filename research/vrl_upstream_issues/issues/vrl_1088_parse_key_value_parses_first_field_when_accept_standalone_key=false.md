# [#1088] parse_key_value parses first field when accept_standalone_key=false

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1088)
- **Status**: `OPEN`
- **Author**: [@pikeas](https://github.com/pikeas)
- **Created At**: `2024-10-23T14:17:25Z`
- **Updated At**: `2026-06-16T13:09:51Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`, `stdlib:parse_key_value`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1088)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

```
parse_key_value("aaa=bbb ccc", accept_standalone_key: false)
```

✅ `could not parse whole line successfully`

```
parse_key_value("aaa bbb=ccc", accept_standalone_key: false)
```

❌ `{"aaa bbb": "ccc"}`

```
parse_key_value("aaa= bbb=ccc", accept_standalone_key: false)
```

❌ `{"aaa": "bbb=ccc"}`

Context: unexpected output when using `parse_logfmt()`, which is a thin wrapper around `parse_key_value()`.
