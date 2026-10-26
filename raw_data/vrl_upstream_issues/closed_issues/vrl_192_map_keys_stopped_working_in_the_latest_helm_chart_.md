# Issue #192: map_keys stopped working in the latest helm chart 0.21

- **URL:** https://github.com/vectordotdev/vrl/issues/192
- **Author:** @oleksiiprokhorenko
- **Status:** CLOSED (completed)
- **Created:** 2023-04-14T15:51:58Z
- **Closed:** 2023-04-20T13:01:38Z
- **Labels:** None

## Description

Hello,

This part of code worked fine on the previous versions:

  de_dots:
      type: remap
    inputs:
    - s3_k8s_logs
    source: |
      . = parse_json!(.message)
      . = map_keys(., recursive: true) -> |key| { replace(key, ".", "_") }
But on the latest helm chart it shows the following error:

2023-04-14T11:12:24.894946Z ERROR vector::topology: Configuration error. error=Transform "de_dots":
error[E121]: type mismatch in closure parameter
┌─ :1:1
│
1 │ . = map_keys(., recursive: true) -> |key| { replace(key, ".", "_") }
│ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
│ │
│ the closure tied to this function call expects a different input value
│ expression has an inferred type of string, integer, float, boolean, null, array or object where an array or object was expected
│
= see language documentation at https://vrl.dev/
= try your code in the VRL REPL, learn more at https://vrl.dev/examples

I'm not sure is this related to VRL or changes in the latest helm chart?
Any suggestions would be appreciated.
