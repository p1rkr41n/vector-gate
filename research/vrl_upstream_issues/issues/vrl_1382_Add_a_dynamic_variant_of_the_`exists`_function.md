# [#1382] Add a dynamic variant of the `exists` function

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1382)
- **Status**: `OPEN`
- **Author**: [@simplepad](https://github.com/simplepad)
- **Created At**: `2025-04-15T20:14:41Z`
- **Updated At**: `2026-06-16T13:09:30Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:exists`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1382)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

Checking if a certain path exists using dynamic values.

### Attempted Solutions

Given an event like this:
```json
{
    "pointer": "bar",
    "foo": {
        "bar": 123
    }
}
```
To check if the path `foo.<pointer>` exists, you could use:
```
.test = !is_null(get!(., ["foo", .pointer]))
```
But that is cumbersome, involves two function calls and won't work if the value stored in `bar` is null.
Playground link with examples of both null and non-null values: [link](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLnRlc3RfbnVtID0gIWlzX251bGwoZ2V0ISguLCBbXCJmb29cIiwgLnBvaW50ZXJfbnVtXSkpXG4udGVzdF9udWxsID0gIWlzX251bGwoZ2V0ISguLCBbXCJmb29cIiwgLnBvaW50ZXJfbnVsbF0pKSIsImV2ZW50Ijp7InBvaW50ZXJfbnVtIjoiYmFyIiwicG9pbnRlcl9udWxsIjoiYmF6IiwiZm9vIjp7ImJhciI6MTIzLCJiYXoiOm51bGx9fSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D)

### Proposal

Add a dynamic variant of the `exists` function, just like `remove` is to `del`.  Unfortunately I don't have a good name for it, could be something like `is_valid` or `is_defined`. The arguments should probably be identical to `remove`, but without `compact`.

### References

_No response_
