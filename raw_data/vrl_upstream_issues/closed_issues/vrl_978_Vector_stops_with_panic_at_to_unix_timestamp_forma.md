# Issue #978: Vector stops with panic at to_unix_timestamp format:nanoseconds VRL function 

- **URL:** https://github.com/vectordotdev/vrl/issues/978
- **Author:** @r3code
- **Status:** CLOSED (completed)
- **Created:** 2024-08-05T10:03:06Z
- **Closed:** 2024-12-09T20:42:20Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->

### Problem


Vector panics at timestamp conversation to_unix_timestamp and crashes. Log messages:

```
vector[582913]: thread 'vector-worker' panicked at 'value can not be represented in a timestamp with nanosecond precision.', /cargo/registry/src/index.crates>
vector[582913]: note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
ox2-vctr-srv01 vector[582913]: thread 'vector-worker' panicked at 'internal error: entered unreachable code: join error or bad poll', src/topology/builder.rs:890:30
ERROR transform{component_kind="transform" component_id=check_unix_timestamp component_type=remap component_n
INFO vector: Vector has stopped.
```

We found out that it was a very small date in some of the logs. This one message has crashed all our 3 aggregators. How: we have Kafka between agents and aggregators, one message crashed first vector and was not consumed, then other two after rebalancing tried to consume this message and also crashed. All 3 aggregators were continuously restarting every 10 seconds, until our fix in VRL.

### Configuration

```text
Vector 0.33.1 
Streaming model (agent - kafka -aggregators)

if exists(.ts) {
      timestampTs , err = parse_timestamp(del(.ts), "%+")
      if err != null {
          .err = err
      } else {
         .Timestamp = to_unix_timestamp(timestampTs, "nanoseconds")
      }
    }
```


### Version

0.33.1

### Debug Output

_No response_

### Example Data


Input: 
"ts": "1677-09-21 00:12:43.145224192Z" - OK. [VRL Playground](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiXG4gICAgaWYgZXhpc3RzKC50cykge1xuICAgICAgdGltZXN0YW1wVHMgLCBlcnIgPSBwYXJzZV90aW1lc3RhbXAoZGVsKC50cyksIFwiJStcIilcbiAgICAgIGlmIGVyciAhPSBudWxsIHtcbiAgICAgICAgICAuZXJyID0gZXJyXG4gICAgICB9IGVsc2Uge1xuICAgICAgICAgICMgaXQgb3ZlcmZsb3dzIHdoZW4gbmFub3NlY29uZHMgaXMgdmVyeSBzbWFsbCBvciBpbnZhbGlkIGRhdGUgXG4gICAgICAgICAgIyBUYWtlIGEgbG9vayBhdCBCcm93c2VyIENvbnNvbGUgXG4gICAgICAgICAgIyAxNjc3LTA5LTIxIDAwOjEyOjQzLjE0NTIyNDE5MlogLT4gLTkyMjMzNzIwMzY4NTQ3NzYwMDAgT0tcbiAgICAgICAgICAjIDE2NzctMDktMjEgMDA6MTI6NDMuMTQ1MjI0MTkxWiAtPiBhbiBlcnJvciBVbmNhdWdodCBSdW50aW1lRXJyb3I6IHVucmVhY2hhYmxlIChwYW5pYylcbiAgICAgICAgICAjIDAwMDAtMDktMjEgMDA6MTI6NDMuMTQ1MjI0MTkxWiAtPiBhbiBlcnJvciBVbmNhdWdodCBSdW50aW1lRXJyb3I6IHVucmVhY2hhYmxlIChwYW5pYylcbiAgICAgICAgICAjIFxuICAgICAgICAgLlRpbWVzdGFtcCA9IHRvX3VuaXhfdGltZXN0YW1wKHRpbWVzdGFtcFRzLCBcIm5hbm9zZWNvbmRzXCIpXG4gICAgICB9XG4gICAgfVxuIiwiZXZlbnQiOnsidHMiOiIxNjc3LTA5LTIxIDAwOjEyOjQzLjE0NTIyNDE5MloifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D)
"ts": "1677-09-21 00:12:43.145224191Z" - Fail. thread 'vector-worker' panicked at 'value can not be represented in a timestamp with nanosecond precision.' [VRL Playground](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiXG4gICAgaWYgZXhpc3RzKC50cykge1xuICAgICAgdGltZXN0YW1wVHMgLCBlcnIgPSBwYXJzZV90aW1lc3RhbXAoZGVsKC50cyksIFwiJStcIilcbiAgICAgIGlmIGVyciAhPSBudWxsIHtcbiAgICAgICAgICAuZXJyID0gZXJyXG4gICAgICB9IGVsc2Uge1xuICAgICAgICAgICMgaXQgb3ZlcmZsb3dzIHdoZW4gbmFub3NlY29uZHMgaXMgdmVyeSBzbWFsbCBvciBpbnZhbGlkIGRhdGUgXG4gICAgICAgICAgIyBUYWtlIGEgbG9vayBhdCBCcm93c2VyIENvbnNvbGUgXG4gICAgICAgICAgIyAxNjc3LTA5LTIxIDAwOjEyOjQzLjE0NTIyNDE5MlogLT4gLTkyMjMzNzIwMzY4NTQ3NzYwMDAgT0tcbiAgICAgICAgICAjIDE2NzctMDktMjEgMDA6MTI6NDMuMTQ1MjI0MTkxWiAtPiBhbiBlcnJvciBVbmNhdWdodCBSdW50aW1lRXJyb3I6IHVucmVhY2hhYmxlIChwYW5pYylcbiAgICAgICAgICAjIDAwMDAtMDktMjEgMDA6MTI6NDMuMTQ1MjI0MTkxWiAtPiBhbiBlcnJvciBVbmNhdWdodCBSdW50aW1lRXJyb3I6IHVucmVhY2hhYmxlIChwYW5pYylcbiAgICAgICAgICAjIFxuICAgICAgICAgLlRpbWVzdGFtcCA9IHRvX3VuaXhfdGltZXN0YW1wKHRpbWVzdGFtcFRzLCBcIm5hbm9zZWNvbmRzXCIpXG4gICAgICB9XG4gICAgfVxuIiwiZXZlbnQiOnsidHMiOiIxNjc3LTA5LTIxIDAwOjEyOjQzLjE0NTIyNDE5MVoifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D)
"ts": "0000-09-21 00:12:43.145224192Z"  - Fail. thread 'vector-worker' panicked at 'value can not be represented in a timestamp with nanosecond precision.' [VRL Playground](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiXG4gICAgaWYgZXhpc3RzKC50cykge1xuICAgICAgdGltZXN0YW1wVHMgLCBlcnIgPSBwYXJzZV90aW1lc3RhbXAoZGVsKC50cyksIFwiJStcIilcbiAgICAgIGlmIGVyciAhPSBudWxsIHtcbiAgICAgICAgICAuZXJyID0gZXJyXG4gICAgICB9IGVsc2Uge1xuICAgICAgICAgICMgaXQgb3ZlcmZsb3dzIHdoZW4gbmFub3NlY29uZHMgaXMgdmVyeSBzbWFsbCBvciBpbnZhbGlkIGRhdGUgXG4gICAgICAgICAgIyBUYWtlIGEgbG9vayBhdCBCcm93c2VyIENvbnNvbGUgXG4gICAgICAgICAgIyAxNjc3LTA5LTIxIDAwOjEyOjQzLjE0NTIyNDE5MlogLT4gLTkyMjMzNzIwMzY4NTQ3NzYwMDAgT0tcbiAgICAgICAgICAjIDE2NzctMDktMjEgMDA6MTI6NDMuMTQ1MjI0MTkxWiAtPiBhbiBlcnJvciBVbmNhdWdodCBSdW50aW1lRXJyb3I6IHVucmVhY2hhYmxlIChwYW5pYylcbiAgICAgICAgICAjIDAwMDAtMDktMjEgMDA6MTI6NDMuMTQ1MjI0MTkxWiAtPiBhbiBlcnJvciBVbmNhdWdodCBSdW50aW1lRXJyb3I6IHVucmVhY2hhYmxlIChwYW5pYylcbiAgICAgICAgICAjIFxuICAgICAgICAgLlRpbWVzdGFtcCA9IHRvX3VuaXhfdGltZXN0YW1wKHRpbWVzdGFtcFRzLCBcIm5hbm9zZWNvbmRzXCIpXG4gICAgICB9XG4gICAgfVxuIiwiZXZlbnQiOnsidHMiOiIwMDAwLTA5LTIxIDAwOjEyOjQzLjE0NTIyNDE5MVoifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D)

Reproduced in VRL Playground
![изображение](https://github.com/user-attachments/assets/d9888a9a-9e76-4cde-87ab-879cca245d12)

### Additional Context

_No response_

### References

https://github.com/vectordotdev/vrl/blob/16889935bf08268547dd494054dc906705a1dfc7/src/stdlib/to_unix_timestamp.rs#L4
```[tasklist]
### Tasks
```

