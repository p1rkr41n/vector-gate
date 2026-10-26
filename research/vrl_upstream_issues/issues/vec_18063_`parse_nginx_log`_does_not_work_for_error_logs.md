# [#18063] `parse_nginx_log` does not work for error logs

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/18063)
- **Status**: `OPEN`
- **Author**: [@fzyzcjy](https://github.com/fzyzcjy)
- **Created At**: `2023-07-22T03:24:12Z`
- **Updated At**: `2026-05-29T23:15:32Z`
- **Comments**: 3
- **Labels**: `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/18063)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Hi thanks for the library! However, it does fail for this message:

```
2023/07/21 08:35:07 [error] 32#32: *29668326 recv() failed (104: Connection reset by peer) while reading response header from upstream, client: 192.168.1.119, server: , request: "GET /what HTTP/1.1", upstream: "http://10.247.225.114:80/what", host: "plusequalone.com"
```

when doing `parse_nginx_log!(.message, "error")`



### Configuration

_No response_

### Version

latest

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
