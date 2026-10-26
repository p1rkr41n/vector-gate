# [#123]  Support non-quoted integer path segments

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/123)
- **Status**: `OPEN`
- **Author**: [@ktff](https://github.com/ktff)
- **Created At**: `2021-04-20T17:06:30Z`
- **Updated At**: `2023-03-28T14:20:26Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:syntax`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/123)

---

## Description

Enable usage of non-quoted integers in path segments. Some examples would be `.0`, `.field.12`, `.2.label` etc...


vectordotdev/vector#7045 enabled usage of non-quoted path identifiers that start with a number. Originally, support for non-quoted integers as path segments was also planned but was scraped once the issues around it became clear and it's usefulness was questioned. 

### Issue
Main issue is `_` chars in integers. Currently the parser will parse `1_000` as an integer and will erase underscores. A naive implementation would use the parsed integer as a key which would result in following `{ "1_000": "a", "1000": "b"}.1_000` to evaluate as `"b"`. 

There are two known approaches:
* Introduce more context into lexer so that it can know when it's in a path so to parse integers as identifiers.
* Raise construction of integers to grammar where we have context. 

Both options would introduce quite the complexity for a feature that is at best a nice to have and at worst could introduce more confusion than it would resolve.

### Alternatives
Quoted integers are supported, `."0"` works, so in the case of not going through with this change no other change is required. 


Follow up on vectordotdev/vector#7045, vectordotdev/vector#6780


