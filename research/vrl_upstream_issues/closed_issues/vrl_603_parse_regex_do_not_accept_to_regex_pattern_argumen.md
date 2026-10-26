# Issue #603: parse_regex do not accept to_regex(...) pattern argument 

- **URL:** https://github.com/vectordotdev/vrl/issues/603
- **Author:** @sxkote
- **Status:** CLOSED (not_planned)
- **Created:** 2023-12-20T12:26:10Z
- **Closed:** 2023-12-20T14:40:35Z
- **Labels:** None

## Description

That code works fine, because, the pattern is regex expression:
`.res = parse_regex(.message, r'.*program') ?? "not found"`

but if i want to use some expression within the pattern is causes multiple errors:
`.res = parse_regex(.message, to_regex(".*program") ?? r'') ?? "not found"`

error: unexpected expression for argument "pattern"
  │        expected: regex
  │        received: operation

for comparison, the same expression will work in match function
