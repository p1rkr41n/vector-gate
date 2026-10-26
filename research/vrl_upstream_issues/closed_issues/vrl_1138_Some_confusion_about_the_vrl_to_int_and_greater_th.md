# Issue #1138: Some confusion about the vrl to_int and greater than documentation

- **URL:** https://github.com/vectordotdev/vrl/issues/1138
- **Author:** @paomian
- **Status:** CLOSED (completed)
- **Created:** 2024-11-25T07:43:01Z
- **Closed:** 2024-11-26T03:40:08Z
- **Labels:** None

## Description

vector version: timberio/vector:0.42.0-debian
I have this example toml to test `drop_in_abort`
```toml
[sources.demo_source]
type = "demo_logs"
format = "apache_common"
lines = [ "line1" ]

[transforms.transform_nginx_log]
type = "remap"
inputs = [ "demo_source" ]
drop_on_error = true
drop_on_abort = true
reroute_dropped = true
source = """
log = parse_apache_log!(.message,format: "common")
if to_int(log.status) > 200 {
  abort
}
. = log
.mark = "transform_nginx_log"
"""

[sinks.transform_nginx_log_sink]
type = "console"
inputs = [ "transform_nginx_log" ]
encoding.codec = "json"


[transforms.transform_nginx_log_dropped]
type = "remap"
inputs = [ "transform_nginx_log.dropped" ]
source = """
.mark = "dropped"
"""

[sinks.dropped_msg_sink]
type = "console"
inputs = [ "transform_nginx_log_dropped" ]
encoding.codec = "json"
```

But when writing the vrl for transform_nginx_log, I'm a bit confused.
my first version is 
```
log = parse_apache_log!(.message,format: "common")
if log.status > 200 {
  abort
}
```
but I got error
```
error[E100]: fallible predicate
  ┌─ :2:4
  │
2 │ if log.status > 200 {
  │    ^^^^^^^^^^^^^^^^
  │    │
  │    expression can result in runtime error
  │    handle the error case to ensure runtime success
```
Ok,I think it's vrl thinks the type of log.status is uncertain, so I'm going to use to_int to convert the type of log.status. So I followed the [documentation](https://vector.dev/docs/reference/vrl/functions/#to_int) and wrote a second version.
```
log = parse_apache_log!(.message,format: "common")
if to_int!(log.status) > 200 {
  abort
}
```
I got a new error.
```
error[E620]: can't abort infallible function
  ┌─ :2:4
  │
2 │ if to_int!(log.status) > 200 {
  │    ^^^^^^- remove this abort-instruction
  │    │
  │    this function can't fail
```
I'm not sure if I'm missing any content. The documentation says that `to_int` is failable.
Eventually I got a usable version.
```
if to_int(log.status) > 200 {
  abort
}
```
Is there a problem I'm overlooking?
