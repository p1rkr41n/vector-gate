# Issue #373: Fix VRL error message - use %vector instead of @vector

- **URL:** https://github.com/vectordotdev/vrl/issues/373
- **Author:** @pront
- **Status:** CLOSED (completed)
- **Created:** 2023-08-07T13:40:01Z
- **Closed:** 2023-08-07T16:09:28Z
- **Labels:** None

## Description

Based on the feedback [here](https://github.com/vectordotdev/vector/discussions/17889#discussioncomment-6646177), the error message incorrectly suggests `@vector` instead of `%vector`.

```
error[E103]: unhandled fallible assignment
  ┌─ :1:7
  │
1 │ .ts = to_unix_timestamp(%vector.ingest_timestamp)
  │ ----- ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  │ │     │
  │ │     this expression is fallible
  │ │     update the expression to be infallible
  │ or change this to an infallible assignment:
  │ .ts, err = to_unix_timestamp(@vector.ingest_timestamp)
```
