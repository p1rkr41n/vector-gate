# [#406] Restore `parse_nginx_log` parsing of the request string, optionally

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/406)
- **Status**: `OPEN`
- **Author**: [@rbarrois](https://github.com/rbarrois)
- **Created At**: `2023-08-21T09:36:10Z`
- **Updated At**: `2026-06-16T13:10:24Z`
- **Comments**: 2
- **Labels**: `stdlib:parse_nginx_log`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/406)

---

## Description

The change in #249 has removed the fields `method`, `path` and `protocol` from the result of `parse_nginx_log`, as the request string might not be parsed.

However, that data is often useful; instead of forcing users of Vector to reimplement that feature as a custom regex, I suggest restoring the parsing of those fields, as an optional behaviour.

This could either be done through returning `null` values for those fields, or through a dedicated `parse_http_request` VRL function.

If there is interest for one of those options, I would happily provide the related changes.
