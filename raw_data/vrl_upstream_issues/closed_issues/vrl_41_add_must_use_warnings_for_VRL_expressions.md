# Issue #41: add "must use" warnings for VRL expressions

- **URL:** https://github.com/vectordotdev/vrl/issues/41
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2022-07-20T18:17:32Z
- **Closed:** 2023-10-20T19:59:25Z
- **Labels:** vrl:diagnostic

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Many expressions / functions in VRL return a result rather than modify the input. For example, the `push` function which appends a single element to the end of an array. It is easy to incorrectly assume this may modify the input, and not check the output which results in the expression doing nothing. We could add `#[must_use]` style warnings to VRL to help prevent these types of issues.


### Example user error
```coffeescript
$ .array = []
[]

$ push(.array, "foo")
["foo"]

$ .array
[]
```


### Version

0.23.0
