# Issue #1742: Unexpected "unused variable"

- **URL:** https://github.com/vectordotdev/vrl/issues/1742
- **Author:** @rienafairefr
- **Status:** CLOSED (completed)
- **Created:** 2026-04-19T20:44:15Z
- **Closed:** 2026-04-24T17:52:27Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem


Using vector (0.54), a transform wasn't compiling and I wasn't really understanding the error message. I managed to distill it down to this minimal example : (you can use any fallible function, I used to_float as an example)

When compiled and run : adding it to the `fixme` folder and running `cargo run --package vrl-tests --bin vrl-tests -- --pattern 'fixme'`

we get this compile error

```
warning[E900]: unused variable `err`
  ┌─ :1:4
  │
1 │ p, err = to_float(.message)
  │    ^^^ help: use the result of this expression or remove it
  │
  = this expression has no side-effects
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```
The `err` variable is used though 🤔  (we assign .e to its value)

The compile error goes away when removing the err = "" line, which suggests to me that it might be an unexpected scoping rule, and the reassignement of the err variable interferes with the "unused code analysis"

The error also does not appear on the VRL playground, only when running `vector` ( or a vrl unit test)


### VRL Program

```text
p, err = to_float(.message)

.p = p
.e = err

err = ""
```

### VRL and/or Vector Version

0.54

### Debug Output

```text

```

### Example

_No response_

### Additional Context

_No response_

### References

_No response_
