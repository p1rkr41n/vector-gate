# [#77] VRL doesn't report fallibility well for statements in blocks

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/77)
- **Status**: `OPEN`
- **Author**: [@StephenWakely](https://github.com/StephenWakely)
- **Created At**: `2022-03-01T18:03:06Z`
- **Updated At**: `2026-06-01T14:05:13Z`
- **Comments**: 0
- **Labels**: `vrl:diagnostic`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/77)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Take this ridiculous VRL script:

```
    if true {
      3 / 0
      # lots of things
      true
    }
```

This error gets reported as:

```
error[E100]: unhandled error
  ┌─ :1:3
  │
1 │ ╭ ╭   if true {
2 │ │ │     3 / 0
3 │ │ │     # lots of things
4 │ │ │     true
5 │ │ │   }
  │ ╰─│───^ expression can result in runtime error
  │   ╰───' handle the error case to ensure runtime success
  │
```

ie. The entire block is reported as "can result in runtime error". 

It would be much more useful if it could actually report the exact statements (in this case the `3 / 0`) within the block that could result in an error.


This issue is slightly complicated by the fact that one can handle the errors within blocks. Eg, this script:

```
    x = {
      3 / 0
      # lots of things
      true
    } ?? true
```

Currently fallibility in a statement is a simple boolean, the solution may require making fallibility a more complex struct that includes the location of the offending statement(s) that get's bubbled up past the blocks.


### Version

v0.20


