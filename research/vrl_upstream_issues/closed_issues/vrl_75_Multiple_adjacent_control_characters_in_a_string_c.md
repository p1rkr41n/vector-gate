# Issue #75: Multiple adjacent control characters in a string cause parsing to produce incorrect results

- **URL:** https://github.com/vectordotdev/vrl/issues/75
- **Author:** @darora
- **Status:** CLOSED (completed)
- **Created:** 2022-03-08T06:13:46Z
- **Closed:** 2026-05-01T18:28:50Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Correct functioning, when control chars are not adjacent:
```
$ parse_logfmt!(s'msg="foo bar\n \nbaz"')
{ "msg": "foo bar\\n \\nbaz" }
```

Incorrect functioning, when control chars are adjacent:
```
$ parse_logfmt!(s'msg="foo bar\n\nbaz"')
{ "bar\n\nbaz"": true, "msg": "\"foo" }

$ parse_logfmt!(s'msg="foo bar\a\abaz"')
{ "bar\a\abaz"": true, "msg": "\"foo" }
```

### Configuration

```text
n/a
```


### Version

vector 0.20.0 (x86_64-apple-darwin 2a706a3 2022-02-10)

### Debug Output

_No response_

### Example Data

`msg="foo bar\a\abaz"`

### Additional Context

_No response_

### References

_No response_
