# Issue #1479: The AWS ALB log format has changed again!

- **URL:** https://github.com/vectordotdev/vrl/issues/1479
- **Author:** @byronwolfman
- **Status:** CLOSED (completed)
- **Created:** 2025-08-19T21:56:00Z
- **Closed:** 2025-08-25T19:01:37Z
- **Labels:** vrl:stdlib, stdlib:parse

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

Vector started getting upset about this a few hours ago:

```
"function call error for \"parse_aws_alb_log\" at (4:32): Log should be fully consumed: \" \"-\" \"-\" \"-\"\""
```

Sure enough, the format has changed! Not universally, but somewhere around 1% of our logs have new elements after the TID:

```
https 2025-08-19T21:34:47.383127Z some/alb/target 1.23.45.67:12345 10.20.30.40:8080 0.010 0.005 0.000 200 200 496 340 "GET https://example.com:443/url/path HTTP/1.1" "User/Agent" SSL-CIPHERS TLSv1.2 arn:aws:elasticloadbalancing:us-feast-1:123456789012:targetgroup/target-group-name/some-id "Root=1-12345678-123456789012345678901234" "example.com" "arn:aws:acm:us-best-2:123456789012:certificate/12345678-1234-1234-1234-123456789012" 20 2025-08-19T21:34:47.367000Z "some_action,forward" "-" "-" "10.20.30.40:8080" "200" "-" "-" TID_12345678901234567890123456789012 "-" "-" "-"
```

^ The above has been heavily anonymized, but the punchline is the part after the TID. Compare this to a log from AWS' [own documentation](https://docs.aws.amazon.com/elasticloadbalancing/latest/application/load-balancer-access-logs.html#access-log-entry-examples) that I'm looking at _right this moment_ that does not yet describe the new elements:

```
http 2018-07-02T22:23:00.186641Z app/my-loadbalancer/50dc6c495c0c9188 
192.168.131.39:2817 10.0.0.1:80 0.000 0.001 0.000 200 200 34 366 
"GET http://www.example.com:80/ HTTP/1.1" "curl/7.46.0" - - 
arn:aws:elasticloadbalancing:us-east-2:123456789012:targetgroup/my-targets/73e2d6bc24d8a067
"Root=1-58337262-36d228ad5d99923122bbe354" "-" "-" 
0 2018-07-02T22:22:48.364000Z "forward" "-" "-" "10.0.0.1:80" "200" "-" "-" TID_1234abcd5678ef90
```

In the AWS example, `TID_1234abcd5678ef90` is the last element. What are the new mystery elements? Who knows! I suppose they might contain values other than `-` in the future, but for now I haven't seen any information about them.

Sample VRL program below demonstrates a parseable log where the last element is the TID is the last element, and can be parsed, and another log that is unparseable because of the new elements.

Vector version taken from whatever was running on VRL playground today.

### VRL Program

```text
parseable = "https 2025-08-19T21:34:47.383127Z some/alb/target 1.23.45.67:12345 10.20.30.40:8080 0.010 0.005 0.000 200 200 496 340 \"GET https://example.com:443/url/path HTTP/1.1\" \"User/Agent\" SSL-CIPHERS TLSv1.2 arn:aws:elasticloadbalancing:us-feast-1:123456789012:targetgroup/target-group-name/some-id \"Root=1-12345678-123456789012345678901234\" \"example.com\" \"arn:aws:acm:us-best-2:123456789012:certificate/12345678-1234-1234-1234-123456789012\" 20 2025-08-19T21:34:47.367000Z \"some_action,forward\" \"-\" \"-\" \"10.20.30.40:8080\" \"200\" \"-\" \"-\" TID_12345678901234567890123456789012"
unparseable = "https 2025-08-19T21:34:47.383127Z some/alb/target 1.23.45.67:12345 10.20.30.40:8080 0.010 0.005 0.000 200 200 496 340 \"GET https://example.com:443/url/path HTTP/1.1\" \"User/Agent\" SSL-CIPHERS TLSv1.2 arn:aws:elasticloadbalancing:us-feast-1:123456789012:targetgroup/target-group-name/some-id \"Root=1-12345678-123456789012345678901234\" \"example.com\" \"arn:aws:acm:us-best-2:123456789012:certificate/12345678-1234-1234-1234-123456789012\" 20 2025-08-19T21:34:47.367000Z \"some_action,forward\" \"-\" \"-\" \"10.20.30.40:8080\" \"200\" \"-\" \"-\" TID_12345678901234567890123456789012 \"-\" \"-\" \"-\""

# This succeeds!
.good = parse_aws_alb_log!(parseable)

# This does not!
.bad, err = parse_aws_alb_log(unparseable)
if err != null {
  .error = "could not parse the unparseable"
  .error_msg = err
}
```

### VRL and/or Vector Version

40d3f6dfa395ef5dd306432e6cfd03af9966da00

### Debug Output

```text

```

### Example

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoicGFyc2VhYmxlID0gXCJodHRwcyAyMDI1LTA4LTE5VDIxOjM0OjQ3LjM4MzEyN1ogc29tZS9hbGIvdGFyZ2V0IDEuMjMuNDUuNjc6MTIzNDUgMTAuMjAuMzAuNDA6ODA4MCAwLjAxMCAwLjAwNSAwLjAwMCAyMDAgMjAwIDQ5NiAzNDAgXFxcIkdFVCBodHRwczovL2V4YW1wbGUuY29tOjQ0My91cmwvcGF0aCBIVFRQLzEuMVxcXCIgXFxcIlVzZXIvQWdlbnRcXFwiIFNTTC1DSVBIRVJTIFRMU3YxLjIgYXJuOmF3czplbGFzdGljbG9hZGJhbGFuY2luZzp1cy1mZWFzdC0xOjEyMzQ1Njc4OTAxMjp0YXJnZXRncm91cC90YXJnZXQtZ3JvdXAtbmFtZS9zb21lLWlkIFxcXCJSb290PTEtMTIzNDU2NzgtMTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0XFxcIiBcXFwiZXhhbXBsZS5jb21cXFwiIFxcXCJhcm46YXdzOmFjbTp1cy1iZXN0LTI6MTIzNDU2Nzg5MDEyOmNlcnRpZmljYXRlLzEyMzQ1Njc4LTEyMzQtMTIzNC0xMjM0LTEyMzQ1Njc4OTAxMlxcXCIgMjAgMjAyNS0wOC0xOVQyMTozNDo0Ny4zNjcwMDBaIFxcXCJzb21lX2FjdGlvbixmb3J3YXJkXFxcIiBcXFwiLVxcXCIgXFxcIi1cXFwiIFxcXCIxMC4yMC4zMC40MDo4MDgwXFxcIiBcXFwiMjAwXFxcIiBcXFwiLVxcXCIgXFxcIi1cXFwiIFRJRF8xMjM0NTY3ODkwMTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMlwiXG51bnBhcnNlYWJsZSA9IFwiaHR0cHMgMjAyNS0wOC0xOVQyMTozNDo0Ny4zODMxMjdaIHNvbWUvYWxiL3RhcmdldCAxLjIzLjQ1LjY3OjEyMzQ1IDEwLjIwLjMwLjQwOjgwODAgMC4wMTAgMC4wMDUgMC4wMDAgMjAwIDIwMCA0OTYgMzQwIFxcXCJHRVQgaHR0cHM6Ly9leGFtcGxlLmNvbTo0NDMvdXJsL3BhdGggSFRUUC8xLjFcXFwiIFxcXCJVc2VyL0FnZW50XFxcIiBTU0wtQ0lQSEVSUyBUTFN2MS4yIGFybjphd3M6ZWxhc3RpY2xvYWRiYWxhbmNpbmc6dXMtZmVhc3QtMToxMjM0NTY3ODkwMTI6dGFyZ2V0Z3JvdXAvdGFyZ2V0LWdyb3VwLW5hbWUvc29tZS1pZCBcXFwiUm9vdD0xLTEyMzQ1Njc4LTEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIzNFxcXCIgXFxcImV4YW1wbGUuY29tXFxcIiBcXFwiYXJuOmF3czphY206dXMtYmVzdC0yOjEyMzQ1Njc4OTAxMjpjZXJ0aWZpY2F0ZS8xMjM0NTY3OC0xMjM0LTEyMzQtMTIzNC0xMjM0NTY3ODkwMTJcXFwiIDIwIDIwMjUtMDgtMTlUMjE6MzQ6NDcuMzY3MDAwWiBcXFwic29tZV9hY3Rpb24sZm9yd2FyZFxcXCIgXFxcIi1cXFwiIFxcXCItXFxcIiBcXFwiMTAuMjAuMzAuNDA6ODA4MFxcXCIgXFxcIjIwMFxcXCIgXFxcIi1cXFwiIFxcXCItXFxcIiBUSURfMTIzNDU2Nzg5MDEyMzQ1Njc4OTAxMjM0NTY3ODkwMTIgXFxcIi1cXFwiIFxcXCItXFxcIiBcXFwiLVxcXCJcIlxuXG4jIFRoaXMgc3VjY2VlZHMhXG4uZ29vZCA9IHBhcnNlX2F3c19hbGJfbG9nIShwYXJzZWFibGUpXG5cbiMgVGhpcyBkb2VzIG5vdCFcbi5iYWQsIGVyciA9IHBhcnNlX2F3c19hbGJfbG9nKHVucGFyc2VhYmxlKVxuaWYgZXJyICE9IG51bGwge1xuICAuZXJyb3IgPSBcImNvdWxkIG5vdCBwYXJzZSB0aGUgdW5wYXJzZWFibGVcIlxuICAuZXJyb3JfbXNnID0gZXJyXG59IiwiZXZlbnQiOnt9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

### Additional Context

_No response_

### References

AWS has launched surprise new log elements before: https://github.com/vectordotdev/vrl/issues/852
