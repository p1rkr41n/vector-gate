# [#1244] parse_json in VRL doesn't support json-like strings (with single quotes)

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1244)
- **Status**: `OPEN`
- **Author**: [@nomalord](https://github.com/nomalord)
- **Created At**: `2025-01-30T23:26:44Z`
- **Updated At**: `2026-06-16T13:09:41Z`
- **Comments**: 3
- **Labels**: `vrl:stdlib`, `stdlib:parse_json`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1244)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I have encountered an issue with parsing json strings with single quotes:
the following VRL expression:
```
.bad = parse_json!(.bad)
```
parsing the following event:
```
{
    bad: "{'test': 'hello'}"
}
```

returns an error saying the json is invalid...

I also tested in the VRL playground
Please help :)
Thanks in advance

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLmJhZCA9IHBhcnNlX2pzb24hKC5iYWQpIiwiZXZlbnQiOm51bGwsImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOiJDb3VsZCBub3QgcGFyc2UgSlNPTiBldmVudDpcbntcbiAgICBiYWQ6IFwieyd0ZXN0JzogJ2hlbGxvJ31cIlxufSJ9

### Configuration

```text

```

### Version

0.38

### Debug Output

```text

```

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
