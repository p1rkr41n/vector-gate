# [#94] Invalid "Exact" Types Can't Be Fixed

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/94)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2021-08-26T12:17:25Z`
- **Updated At**: `2026-06-01T14:05:01Z`
- **Comments**: 0
- **Labels**: `vrl:diagnostic`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/94)

---

## Description

 ```
error[E110]: invalid argument type
  ┌─ :1:8
  │
1 │ upcase(null)
  │        ^^^^
  │        │
  │        this expression resolves to the exact type "null"
  │        but the parameter "value" expects the exact type "string"
  │
  = try: ensuring an appropriate type at runtime
  =
  =     null = string!(null)
  =     upcase(null)
  =
  = try: coercing to an appropriate type and specifying a default value as a fallback in case coercion fails
  =
  =     null = to_string(null) ?? "default"
  =     upcase(null)
  =
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = learn more about error code 110 at https://errors.vrl.dev/110
  = see language documentation at https://vrl.dev
```

The above diagnostic message is nonsensical because `null` can never be forced into a string. Basically, this code can never compile, regardless of what error handling you apply, since it'll always fail at runtime.

Pulled out from https://github.com/timberio/vector/pull/8894.
