# Issue #5: VRL: Add ingress-nginx log format for `parse_nginx_log`

- **URL:** https://github.com/vectordotdev/vrl/issues/5
- **Author:** @esergion
- **Status:** CLOSED (completed)
- **Created:** 2023-03-19T06:41:03Z
- **Closed:** 2023-05-24T01:36:23Z
- **Labels:** vrl:stdlib, good first issue

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Hey guys,

Currently there are only two log formats supported by `parse_nginx_log` function: "combined" and "error".
There's one more ingress-nginx controller default log format described [here](https://kubernetes.github.io/ingress-nginx/user-guide/nginx-configuration/log-format/).

```
log_format upstreaminfo
    '$remote_addr - $remote_user [$time_local] "$request" '
    '$status $body_bytes_sent "$http_referer" "$http_user_agent" '
    '$request_length $request_time [$proxy_upstream_name] [$proxy_alternative_upstream_name] $upstream_addr '
    '$upstream_response_length $upstream_response_time $upstream_status $req_id';
```

While the beginning of the format is pretty much the same as "combined" described [here](https://nginx.org/en/docs/http/ngx_http_log_module.html#log_format):

```
log_format combined '$remote_addr - $remote_user [$time_local] '
                    '"$request" $status $body_bytes_sent '
                    '"$http_referer" "$http_user_agent"';
```
I believe there is an intention to make different default formats to parse them separately, like for example

```
structured, err = parse_nginx_log(.message, "ingress_upstreaminfo")
```

as discussed briefly in this [issue](https://github.com/vectordotdev/vector/issues/6103#issuecomment-762893997)

Anyways, in general it would be much easier for all kubernetes users who uses ingress-nginx in clusters to use `parse_nginx_log` instead of making their own regular expressions for a pretty default log format

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

_No response_

### Version

_No response_
