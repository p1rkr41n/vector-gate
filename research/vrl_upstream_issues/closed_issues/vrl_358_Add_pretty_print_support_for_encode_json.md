# Issue #358: Add pretty print support for encode_json

- **URL:** https://github.com/vectordotdev/vrl/issues/358
- **Author:** @Hexta
- **Status:** CLOSED (completed)
- **Created:** 2023-08-01T10:38:30Z
- **Closed:** 2023-08-07T18:58:36Z
- **Labels:** type:enhancement

## Description

Introducing a `pretty` parameter to the `encode_json` function would be beneficial as it enables pretty print support for JSON output. 
When the `pretty` parameter is set to `true`, the function will utilize `serde_json::to_string_pretty` to generate indented and human-readable JSON. 
Conversely, when `pretty` is set to `false` (or not provided), the function will revert to the original behavior of using `serde_json::to_string` for compact JSON output. 
