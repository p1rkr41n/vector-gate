# [#376] parse_url doesn't support duplicated query parameters

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/376)
- **Status**: `OPEN`
- **Author**: [@anas-aso](https://github.com/anas-aso)
- **Created At**: `2022-02-25T11:03:19Z`
- **Updated At**: `2026-06-16T13:11:13Z`
- **Comments**: 2
- **Labels**: `vrl:stdlib`, `stdlib:parse_url`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/376)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

For URLs like this one `http://exam.co/?key=val1&key=val2` when we use `parse_url` function, only the last value will be returned. 
Having duplicated query parameters is a valid HTTP URL
<img width="1792" alt="Screenshot 2022-02-25 at 11 25 11" src="https://user-images.githubusercontent.com/16538065/155699434-9c1da3b7-ae22-4d97-b4da-adcecc5088c3.png">

This happens because the list of query params is turned in to a map [here](https://github.com/vectordotdev/vector/blob/26b4e959613dd1c6768f11ba2e1ff6e8df0494bd/lib/vrl/stdlib/src/parse_url.rs#L146)

### Configuration

```text
not needed as this is pure VRL.
```


### Version

vector 0.19.2

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
