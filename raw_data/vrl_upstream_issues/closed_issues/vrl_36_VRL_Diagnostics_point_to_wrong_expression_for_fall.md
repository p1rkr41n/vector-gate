# Issue #36: VRL: Diagnostics point to wrong expression for fallibility error

- **URL:** https://github.com/vectordotdev/vrl/issues/36
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2022-08-01T19:39:48Z
- **Closed:** 2026-05-01T20:53:46Z
- **Labels:** vrl:diagnostic, meta:regression

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

In the following example, the `push(.x, 1)` is fallible, but the diagnostic error points to the incorrect expression.

```coffeescript
{
   .a=1
   push(.x,1)
   .b=2
}
```
```text

error[E103]: unhandled fallible assignment
  ┌─ :4:7
  │
4 │    .b=2
  │    -- ^
  │    │  │
  │    │  this expression is fallible
  │    │  update the expression to be infallible
  │    or change this to an infallible assignment:
  │    .b, err = 2
  │
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = learn more about error code 103 at https://errors.vrl.dev/103
  = see language documentation at https://vrl.dev

```


### Version

0.23.0
