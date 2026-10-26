# [#1561] `parse_klog` fails if the message contains newlines

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1561)
- **Status**: `OPEN`
- **Author**: [@Ilmarii](https://github.com/Ilmarii)
- **Created At**: `2025-11-21T04:15:19Z`
- **Updated At**: `2026-06-01T14:08:50Z`
- **Comments**: 0
- **Labels**: `stdlib:parse_klog`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1561)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

The `parse_klog` function panics if a message contains a newline character. Such messages are expected to be parsed correctly.

### VRL Program

```text
.klog = parse_klog!("E1120 21:46:33.051464     777 kuberuntime_manager.go:1341] \"Unhandled Error\" err=<\n\tinit container: not found\n > logger=\"UnhandledError\"")
```

### VRL and/or Vector Version

vector 0.51.1

### Debug Output

```text
error[E000]: function call error for "parse_klog" at (8:166): failed parsing klog message
  ┌─ :1:9
  │
1 │ .klog = parse_klog!("E1120 21:46:33.051464     777 kuberuntime_manager.go:1341] \"Unhandled Error\" err=<\n\tinit container: not found\n > logger=\"UnhandledError\"")
  │         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ failed parsing klog message
  │
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

### Example

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLmtsb2cgPSBwYXJzZV9rbG9nIShcIkUxMTIwIDIxOjQ2OjMzLjA1MTQ2NCAgICAgNzc3IGt1YmVydW50aW1lX21hbmFnZXIuZ286MTM0MV0gXFxcIlVuaGFuZGxlZCBFcnJvclxcXCIgZXJyPTxcXG5cXHRpbml0IGNvbnRhaW5lcjogbm90IGZvdW5kXFxuID4gbG9nZ2VyPVxcXCJVbmhhbmRsZWRFcnJvclxcXCJcIikiLCJldmVudCI6eyJtZXNzYWdlIjoiSGVsbG8gVlJMIiwiZm9vIjoiZGVsZXRlIG1lIiwiaHR0cF9zdGF0dXMiOiIyMDAiLCJwbG9wbG8iOm51bGx9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

### Additional Context

_No response_

### References

_No response_
