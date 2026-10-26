# Issue #187: Allow parse_regex and parse_regex_all to receive as a parameter the result of dynamic to_regex like in match function

- **URL:** https://github.com/vectordotdev/vrl/issues/187
- **Author:** @Genry1
- **Status:** CLOSED (completed)
- **Created:** 2023-02-28T10:15:54Z
- **Closed:** 2026-05-26T18:54:21Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

`parse_regex` and `parse_regex_all` are accepting the parameter to be only regex. Though the regex can be stored in a variable or resolved on the fly by the `to_regex` function. At the moment this is supported only by `match` function.

### Attempted Solutions

Tried in different ways and the only possible option is to pass regex directly as an argument, like: `parse_regex(r'')`

### Proposal

An option to pass the regex parameter as a variable or as a result of another function (so called group). e.g. `parse_regex(to_regex("some_regex"))` or `my_regex = r''; parse_regex(my_regex)`

### References

Here is the issue which introduced the `to_regex` function https://github.com/vectordotdev/vector/issues/7051

### Version

0.28.0
