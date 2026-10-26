# [#60] Make "fallible expression" error in VRL specific for each expression

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/60)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-05-27T05:41:20Z`
- **Updated At**: `2026-06-01T14:16:51Z`
- **Comments**: 1
- **Labels**: `vrl:diagnostic`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/60)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

In vectordotdev/vector#12880, the "expression is fallible" diagnostic is improved to point to the exact expression that is fallible. The next improvement to this would be to make the expression message specific to the type of expression that is fallible.

This would allow us to inform the operator how to handle the fallibility more precisely.

For example, this:

```
error[E100]: unhandled error
   ┌─ :10:5
   │
10 │ 5 + to_int(.foo)
   │     ^^^^^^^^^^^^
   │     │
   │     expression can result in runtime error
   │     handle the error case to ensure runtime success
   │
   = see documentation about error handling at https://errors.vrl.dev/#handling
   = learn more about error code 100 at https://errors.vrl.dev/100
   = see language documentation at https://vrl.dev/
```

Could be rewritten to inform the user of using `to_int!`. Similarly, for rewriting regular assignments to infallible assignments.

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

_No response_

### Version

_No response_
