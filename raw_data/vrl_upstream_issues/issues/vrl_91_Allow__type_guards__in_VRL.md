# [#91] Allow "type guards" in VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/91)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2021-10-01T17:35:46Z`
- **Updated At**: `2023-03-28T13:49:48Z`
- **Comments**: 2
- **Labels**: `type:enhancement`, `vrl:typedef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/91)

---

## Description

I believe we've discussed this in other places before as well, but it came up again in https://github.com/vectordotdev/vector/issues/9406 where a user expected that if they used `is_string()` that VRL would be able to determine that the argument thereafter was a string if the rest of the expression only executed if `is_string` was true.

Specifically, they had:

```
is_string(.message) && !contains(.message, s'test')
```

But you could also imagine this with `if` conditions:

```
if is_string(.message) {
 !contains(.message, s'test')
} else {
  false
}
```

I'm not 100% sold on if we want to do this, but opening for discussion.
