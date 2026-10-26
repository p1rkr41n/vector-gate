# Issue #1149: VRL compiler warns about the unused result of `set_semantic_meaning`

- **URL:** https://github.com/vectordotdev/vrl/issues/1149
- **Author:** @sfackler
- **Status:** CLOSED (completed)
- **Created:** 2024-11-26T02:13:00Z
- **Closed:** 2024-11-27T19:40:27Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

The VRL compiler reports a warning for calls to `set_semantic_meaning`:

```
2024-11-26T02:02:17.453462Z  WARN transform{component_kind="transform" component_id=talos_kernel_logs_cleanup component_type=remap}: vector::transforms::remap: VRL compilation warning. warnings=
warning[E900]: unused result for function call `set_semantic_meaning(."talos-time", "timestamp")`
  ┌─ :1:1
  │
1 │ set_semantic_meaning(."talos-time", "timestamp")
  │ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ help: use the result of this expression or remove it
  │
  = this expression has no side-effects
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

From looking at the docs, it seems to be true that the function has no side effects, but that it also returns no value so the warning seems wrong.

### Configuration

```text
set_semantic_meaning(."talos-time", "timestamp")

del(.clock)
del(.seq)
del(."talos-level")
."talos-time" = parse_timestamp!(."talos-time", "%+")
```


### Version

0.42.0

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
