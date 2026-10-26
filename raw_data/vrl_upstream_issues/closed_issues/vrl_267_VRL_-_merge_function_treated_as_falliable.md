# Issue #267: VRL -> merge function treated as falliable

- **URL:** https://github.com/vectordotdev/vrl/issues/267
- **Author:** @nmiculinic
- **Status:** CLOSED (completed)
- **Created:** 2023-06-16T15:24:33Z
- **Closed:** 2023-06-16T17:51:42Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I have the following VRL:

```
# Parse common formats if possible
structured, err =
    parse_json(.message) ??
    parse_logfmt(.message)

if err == null {
    # This is infaillable, seems to be upstream bug https://vector.dev/docs/reference/vrl/functions/#merge
    . = merge(., structured)
}
```

and upon running it get the following error:

```
  error[E103]: unhandled fallible assignment
    ┌─ :8:9
    │
  8 │     . = merge(., structured)
    │     --- ^^^^^^^^^^^^^^^^^^^^
    │     │   │
    │     │   this expression is fallible
    │     │   update the expression to be infallible
    │     or change this to an infallible assignment:
    │     ., err = merge(., structured)
    │
```

I'm not sure what's the recommended pattern to parse logline formats if possible; and merge accordingly. I could do:
```
., _ = merge(., structured)
```

which makes the VRL pass the compiler check, and it's fine when running unit testing

### Configuration

_No response_

### Version

vector 0.30.0 (x86_64-apple-darwin 38c3f0b 2023-05-22 17:38:48.655488673)

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
