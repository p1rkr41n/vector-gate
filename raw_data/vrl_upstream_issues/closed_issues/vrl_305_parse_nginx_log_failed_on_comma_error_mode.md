# Issue #305: parse_nginx_log failed on comma (error mode)

- **URL:** https://github.com/vectordotdev/vrl/issues/305
- **Author:** @buzzdan
- **Status:** CLOSED (completed)
- **Created:** 2023-07-09T07:58:18Z
- **Closed:** 2025-02-19T20:46:56Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

i'm trying to parse nginx errors with `parse_nginx_log`. 
most of them work ok and few failed to parse. 
when i isolated the problem i saw that it boils down to a single comma:

run this code:
```
structured = parse_nginx_log!(.message,"error")
. = merge(., structured)
```

with this vector event:
```json
{
	"message": "2023/05/31 13:42:28 [notice] 76#76: signal 1 (SIGHUP) received from 138 reconfiguring"
}
```

it will work.

now if we add comma:
```json
{
	"message": "2023/05/31 13:42:28 [notice] 76#76: signal 1 (SIGHUP) received from 138, reconfiguring"
}
```
it will fail.


### Configuration

_No response_

### Version

vector 0.30.0 (x86_64-apple-darwin 38c3f0b 2023-05-22 17:38:48.655488673)

### Debug Output

_No response_

### Example Data

2023/05/31 13:42:34 [notice] 76#76: signal 1 (SIGHUP) received from 138, reconfiguring

### Additional Context

_No response_

### References

playground link:

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoic3RydWN0dXJlZCA9IHBhcnNlX25naW54X2xvZyEoLm1lc3NhZ2UsXCJlcnJvclwiKVxuLiA9IG1lcmdlKC4sIHN0cnVjdHVyZWQpXG4iLCJldmVudCI6eyJtZXNzYWdlIjoiMjAyMy8wNS8zMSAxMzo0MjoyOCBbbm90aWNlXSA3NiM3Njogc2lnbmFsIDEgKFNJR0hVUCkgcmVjZWl2ZWQgZnJvbSAxMzggcmVjb25maWd1cmluZyJ9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

when you run it - it works
now try to add a comma somewhere on the message and run.

like this:

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoic3RydWN0dXJlZCA9IHBhcnNlX25naW54X2xvZyEoLm1lc3NhZ2UsXCJlcnJvclwiKVxuLiA9IG1lcmdlKC4sIHN0cnVjdHVyZWQpXG4iLCJldmVudCI6eyJtZXNzYWdlIjoiMjAyMy8wNS8zMSAxMzo0MjoyOCBbbm90aWNlXSA3NiM3Njogc2lnbmFsIDEgKFNJR0hVUCkgcmVjZWl2ZWQgZnJvbSAxMzgsIHJlY29uZmlndXJpbmcifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D
