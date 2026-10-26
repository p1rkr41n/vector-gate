# [#37] VRL: Runtime `abort` is implicitly converted to a fallible error instead of propagating

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/37)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-07-29T19:40:45Z`
- **Updated At**: `2026-06-01T14:05:59Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/37)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

In all of these examples, the program should be aborted, but instead it continues running. The 2nd example shows how VRL treats the abort as a fallible expression. An `abort` should not be recoverable, and should not be treated as "fallible".
Example 3 shows the expression continues to execute (since the CLI examples don't clearly show aborts)

### Example 1
```coffeescript
$ 43 % {abort} ?? 0
0
```

### Example 2
```coffeescript
$ x, err = 1 + {abort}
"aborted"

$ err
"aborted"
```

### Example 3
```coffeescript
$ {x, err = 1 + {abort}; 5}

5
```


### Version

0.23.0

