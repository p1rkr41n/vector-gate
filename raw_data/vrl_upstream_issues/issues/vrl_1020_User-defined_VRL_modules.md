# [#1020] User-defined VRL modules

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1020)
- **Status**: `OPEN`
- **Author**: [@uralmetal](https://github.com/uralmetal)
- **Created At**: `2024-09-06T12:38:05Z`
- **Updated At**: `2025-09-29T08:28:00Z`
- **Comments**: 6
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1020)

---

## Description

This is an idea for improving reuse and code style VRL. I suggest to realize mechanism like python `import` or Jinja `include`. tthis is necessary to use user vrl code in different pipelines without using the Pipeline to Pipeline communication
For example:

user library
```
function set_http_status_code() {
    http_status_code = parse_int!(.http_status)
    del(.http_status)

    if http_status_code >= 200 && http_status_code <= 299 {
        .status = "success"
    } else {
        .status = "error"
    }
}
```

pipeline code
```
from library import set_http_status_code

del(.foo)

.timestamp = now()

set_http_status_code()

```
 
