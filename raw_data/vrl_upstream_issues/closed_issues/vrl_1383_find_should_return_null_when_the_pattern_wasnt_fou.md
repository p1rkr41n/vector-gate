# Issue #1383: `find` should return `null` when the pattern wasn't found

- **URL:** https://github.com/vectordotdev/vrl/issues/1383
- **Author:** @simplepad
- **Status:** CLOSED (completed)
- **Created:** 2025-04-15T20:27:09Z
- **Closed:** 2025-09-22T19:18:37Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

Discussed in https://github.com/vectordotdev/vrl/discussions/1311

Right now it returns `-1`, which from what I can see is somewhat of a special case, because in other functions if something could not be found, `null` is returned. Returning `-1` might introduce hidden bugs if the return value is not analyzed, for example:

```
input = "foobar"
index = find!(input, "123")
output = slice!(input, index)
assert_eq!(output, "r")
```
This code will compile without issues, and the value stored in `output` will be `"r"`. Maybe it would be better to return `null` (which will fail the `slice!()` function) or make the `find!()` function fail if the pattern wasn't found, requiring the developer to handle that case explicitly.

### VRL Program

```text
input = "foobar"
index = find!(input, "123")
output = slice!(input, index)
assert_eq!(output, "r")
```

### VRL and/or Vector Version

VRL Version: 	0.22.0

### Debug Output

```text

```

### Example

[Playground Link](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiaW5wdXQgPSBcImZvb2JhclwiXG5pbmRleCA9IGZpbmQhKGlucHV0LCBcIjEyM1wiKVxub3V0cHV0ID0gc2xpY2UhKGlucHV0LCBpbmRleClcbmFzc2VydF9lcSEob3V0cHV0LCBcInJcIikiLCJldmVudCI6eyJtZXNzYWdlIjoiSGVsbG8gVlJMIiwiZm9vIjoiZGVsZXRlIG1lIiwiaHR0cF9zdGF0dXMiOiIyMDAifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D)

### Additional Context

_No response_

### References

Discussed in https://github.com/vectordotdev/vrl/discussions/1311
