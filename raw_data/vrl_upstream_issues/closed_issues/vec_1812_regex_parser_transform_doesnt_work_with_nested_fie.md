# Issue #1812: `regex_parser` transform doesn't work with nested fields

- **URL:** https://github.com/vectordotdev/vector/issues/1812
- **Author:** @ghost
- **Status:** CLOSED (completed)
- **Created:** 2020-02-16T18:52:38Z
- **Closed:** 2021-01-04T19:12:30Z
- **Labels:** good first issue, needs:approval, domain:vrl

## Description

Currently the `regex` crate which underlies our `regex_parser` implementation supports only `[_0-9a-zA-Z]+` as possible names for captures groups. Thus nested fields of form `x.y.z` cannot be captured.

For example, the following config unit test

```toml
[transforms.regex_parser_nested]
  inputs = []
  type = "regex_parser"
  regex = "^(?P<nested.timestamp>[\\w\\-:\\+]+) (?P<nested.level>\\w+) (?P<doubly.nested.message>.*)$"
[[tests]]
  name = "regex_parser_nested"
  [tests.input]
    insert_at = "regex_parser_nested"
    type = "raw"
    value = "2020-01-01T12:34:56Z INFO hello"
  [[tests.outputs]]
    extract_from = "regex_parser_nested"
    [[tests.outputs.conditions]]
      type = "check_fields"
      "nested.timestamp.equals" = "2020-01-01T12:34:56Z"
      "nested.level.equals" = "INFO"
      "doubly.nested.message.equals" = "hello"
```

fails with the error

```
Failed to build test 'regex_parser_nested':
  failed to build transform 'regex_parser_nested': Invalid regular expression: regex parse error:
      ^(?P<nested.timestamp>[\w\-:\+]+) (?P<nested.level>\w+) (?P<doubly.nested.message>.*)$
                 ^
  error: invalid capture group character
```

I think we need to allow field names containing dots. A simplest option to do this is to fork the `regex` crate and add support for it there, send a PR to the upstream, and use the fork until the support for dots in capture groups in added to the upstream crate.
