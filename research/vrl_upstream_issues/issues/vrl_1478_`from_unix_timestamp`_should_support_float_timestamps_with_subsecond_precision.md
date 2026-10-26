# [#1478] `from_unix_timestamp` should support float timestamps with subsecond precision

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1478)
- **Status**: `OPEN`
- **Author**: [@garysassano](https://github.com/garysassano)
- **Created At**: `2025-08-19T19:19:37Z`
- **Updated At**: `2026-06-16T13:09:21Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`, `stdlib:from_unix_timestamp`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1478)

---

## Description

## Summary

The `from_unix_timestamp` function in Vector's VRL only accepts integer values, which requires unnecessary and error-prone conversions when working with float Unix timestamps that include subsecond precision (e.g., from Caddy logs: `1692470616.525887`).

## Current Behavior

Currently, `from_unix_timestamp` has this signature:

```
from_unix_timestamp(value: <integer>, [unit: <string>]) :: <timestamp>
```

This means when you have a float timestamp like `1692470616.525887`, you cannot use it directly and must perform manual conversion:

```vrl
# Current workaround - verbose and error-prone
timestamp_ns = to_int(float!(.ts) * 1000000000)
.Timestamp = from_unix_timestamp!(timestamp_ns, unit: "nanoseconds")
```

## Expected Behavior

The function should accept both integer and float values, automatically handling the conversion:

```vrl
# Should work directly
.Timestamp = from_unix_timestamp!(.ts)  # Where .ts is 1692470616.525887

# Or with explicit unit specification
.Timestamp = from_unix_timestamp!(.ts, unit: "nanoseconds")
```

## Proposed Solution

Update the function signature to:

```text
from_unix_timestamp(value: <integer | float>, [unit: <string>]) :: <timestamp>
```

When a float is provided:

- For `unit: "seconds"` (default): convert to `DateTime`, discarding the subsecond precision
- For `unit: "milliseconds"`: convert to `DateTime64(6)`
- For `unit: "nanoseconds"`: convert to `DateTime64(9)`

## Environment

- **Vector version**: 0.47.0
- **Platform**: AL2023 on EC2
