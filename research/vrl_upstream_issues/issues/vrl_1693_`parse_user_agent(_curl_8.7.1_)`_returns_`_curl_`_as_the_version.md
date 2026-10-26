# [#1693] `parse_user_agent("curl/8.7.1")` returns `"curl"` as the version

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1693)
- **Status**: `OPEN`
- **Author**: [@andrey-mazo](https://github.com/andrey-mazo)
- **Created At**: `2026-03-09T17:37:21Z`
- **Updated At**: `2026-06-16T13:09:15Z`
- **Comments**: 0
- **Labels**: `stdlib:parse_user_agent`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1693)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

I find it rather confusing for `parse_user_agent("curl/8.7.1")` and especially for `parse_user_agent("curl/8.7.1", mode: "enriched")` to set `browser.version` to `"curl"` instead of `"8.7.1"`,
despite correctly extracting major/minor/patch versions in the enriched mode.

is this intentional or a bug?

```
$ parse_user_agent("curl/8.7.1")
{ "browser": { "family": "HTTP Library", "version": "curl" }, "device": { "category": "misc" }, "os": { "family": null, "version": null } }

$ parse_user_agent("curl/8.7.1", mode: "enriched")
{ "browser": { "family": "curl", "major": "8", "minor": "7", "patch": "1", "version": "curl" }, "device": { "brand": null, "category": "misc", "family": null, "model": null }, "os": { "family": null, "major": null, "minor": null, "patch": null, "patch_minor": null, "version": null } }
```

### VRL Program

```text
parse_user_agent("curl/8.7.1")

parse_user_agent("curl/8.7.1", mode: "enriched")
```

### VRL and/or Vector Version

0.53.0

### Debug Output

```text

```

### Example

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLnVzZXJfYWdlbnQuZmFzdCA9IHBhcnNlX3VzZXJfYWdlbnQhKC51c2VyX2FnZW50X3N0cmluZylcbi51c2VyX2FnZW50LmVucmljaGVkID0gcGFyc2VfdXNlcl9hZ2VudCEoLnVzZXJfYWdlbnRfc3RyaW5nLCBtb2RlOiBcImVucmljaGVkXCIpXG4udXNlcl9hZ2VudC5yZWxpYWJsZSA9IHBhcnNlX3VzZXJfYWdlbnQhKC51c2VyX2FnZW50X3N0cmluZywgbW9kZTogXCJyZWxpYWJsZVwiKSIsImV2ZW50Ijp7InVzZXJfYWdlbnRfc3RyaW5nIjoiY3VybC84LjcuMSJ9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

### Additional Context

_No response_

### References

_No response_
