# [#24] Code suggestions can suggest writing to immutable fields

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/24)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-09-15T19:31:58Z`
- **Updated At**: `2026-06-01T14:06:18Z`
- **Comments**: 0
- **Labels**: `vrl:diagnostic`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/24)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

A [user in Discord](https://discord.com/channels/742820443487993987/1020017447568424960/1020042153667350568) was trying to write a VRL condition, but it complained the input to a function might not be a string, so it suggested modifying the input first with `.message = string!(.message)`. This would normally work, except in conditions the event cannot be mutated. The suggestion could instead be inlined in the function, or maybe use local variables which are never (currently) read only.

Original VRL code
```coffee
!contains(.message, "ELB-HealthChecker")
```

```
error[E110]: invalid argument type
  ┌─ :1:11
  │
1 │ !contains(.message, "ELB-HealthChecker")
  │           ^^^^^^^^
  │           │
  │           this expression resolves to any
  │           but the parameter "value" expects the exact type string
  │
  = try: ensuring an appropriate type at runtime
  =
  =     .message = string!(.message)
  =     contains(.message, "ELB-HealthChecker")
  =
  = try: coercing to an appropriate type and specifying a default value as a fallback in case coercion fails
  =
  =     .message = to_string(.message) ?? "default"
  =     contains(.message, "ELB-HealthChecker")
  =
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = learn more about error code 110 at https://errors.vrl.dev/110
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```


Suggested Change
```coffee
.message = string!(.message)
!contains(.message, "ELB-HealthChecker")
```

```
error[E315]: mutation of read-only value                                                                                                                                                                         │
│   ┌─ :1:1                                                                                                                                                                                                        │
│   │                                                                                                                                                                                                              │
│ 1 │ .message = string!(.message)                                                                                                                                                                                 │
│   │ ^^^^^^^^^^ mutation of read-only value                                                                                                                                                                       │
│   │                                                                                                                                                                                                              │
│   = see language documentation at https://vrl.dev                                                                                                                                                                │
│   = try your code in the VRL REPL, learn more at https://vrl.dev/examples                                                                                                                                        │
│                                                                                                                                                                                                                  │
│ error[E110]: invalid argument type                                                                                                                                                                               │
│   ┌─ :2:10                                                                                                                                                                                                       │
│   │                                                                                                                                                                                                              │
│ 2 │ contains(.message, "ELB-HealthChecker")                                                                                                                                                                      │
│   │          ^^^^^^^^                                                                                                                                                                                            │
│   │          │                                                                                                                                                                                                   │
│   │          this expression resolves to any                                                                                                                                                                     │
│   │          but the parameter "value" expects the exact type string                                                                                                                                             │
│   │                                                                                                                                                                                                              │
│   = try: ensuring an appropriate type at runtime                                                                                                                                                                 │
│   =                                                                                                                                                                                                              │
│   =     .message = string!(.message)                                                                                                                                                                             │
│   =     contains(.message, "ELB-HealthChecker")                                                                                                                                                                  │
│   =                                                                                                                                                                                                              │
│   = try: coercing to an appropriate type and specifying a default value as a fallback in case coercion fails                                                                                                     │
│   =                                                                                                                                                                                                              │
│   =     .message = to_string(.message) ?? "default"                                                                                                                                                              │
│   =     contains(.message, "ELB-HealthChecker")                                                                                                                                                                  │
│   =                                                                                                                                                                                                              │
│   = see documentation about error handling at https://errors.vrl.dev/#handling                                                                                                                                   │
│   = learn more about error code 110 at https://errors.vrl.dev/110                                                                                                                                                │
│   = see language documentation at https://vrl.dev                          
```


Correct suggestion
```coffee
!contains(string!(.message), "ELB-HealthChecker")
```


### Version

0.24.0

