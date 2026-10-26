# Issue #522: parse_nginx_log fails on -

- **URL:** https://github.com/vectordotdev/vrl/issues/522
- **Author:** @mtekel
- **Status:** CLOSED (completed)
- **Created:** 2023-10-24T11:01:50Z
- **Closed:** 2023-10-27T19:47:03Z
- **Labels:** None

## Description

Using parse_nginx_log function, ingress_upstreaminfo format, parsing fails if one of 3 pre-last (that is, 4., 3., 2nd field from the end) contain hyphen, even though according to parsing regex definition this should work:

https://github.com/ex5/vrl/blob/e92c778d62072cf993992167f08f60ca47162abc/src/stdlib/log_util.rs#L145-L147

Example program: https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoic3RydWN0dXJlZCA9IHBhcnNlX25naW54X2xvZyEoLm1lc3NhZ2UsXCJpbmdyZXNzX3Vwc3RyZWFtaW5mb1wiKVxuLiA9IG1lcmdlKC4sIHN0cnVjdHVyZWQpXG4iLCJldmVudCI6eyJtZXNzYWdlIjoiLSAtIC0gWzAzL09jdC8yMDIzOjE0OjIxOjM2ICswMDAwXSBcIlBPU1QgLyBIVFRQLzEuMVwiIDQ5OSAwIFwiLVwiIFwiLVwiIDExMjggMC4wMDMgW3NvbWUuYWRkcmVzcy5jb21dIFstXSBodHRwcyAwIDAuMDA0IDAwNSAxMC41My4xMzQuNDcifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D

If you change 3rd field before end, from 0.004 to e.g. 004, then you get error, meaning it is trying to match against regex rule that defines it has to have a dot. Interestingly, same rule defines optional -, but if you change this field into -, then it fails:

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoic3RydWN0dXJlZCA9IHBhcnNlX25naW54X2xvZyEoLm1lc3NhZ2UsXCJpbmdyZXNzX3Vwc3RyZWFtaW5mb1wiKVxuLiA9IG1lcmdlKC4sIHN0cnVjdHVyZWQpXG4iLCJldmVudCI6eyJtZXNzYWdlIjoiLSAtIC0gWzAzL09jdC8yMDIzOjE0OjIxOjM2ICswMDAwXSBcIlBPU1QgLyBIVFRQLzEuMVwiIDQ5OSAwIFwiLVwiIFwiLVwiIDExMjggMC4wMDMgW3NvbWUuYWRkcmVzcy5jb21dIFstXSBodHRwcyAwIC0gMDA1IDEwLjUzLjEzNC40NyJ9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

VRL:
```
structured = parse_nginx_log!(.message,"ingress_upstreaminfo")
. = merge(., structured)
```

Log message:
```
{
	"message": "- - - [03/Oct/2023:14:21:36 +0000] \"POST / HTTP/1.1\" 499 0 \"-\" \"-\" 1128 0.003 [some.address.com] [-] https 0 - 005 10.53.134.47"
}
```

Vector version 0.33
