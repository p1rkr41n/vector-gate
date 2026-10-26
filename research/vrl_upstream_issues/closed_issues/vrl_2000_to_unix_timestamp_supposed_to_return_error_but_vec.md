# Issue #2000: to_unix_timestamp supposed to return error but vector compiler indicates that's not true

- **URL:** https://github.com/vectordotdev/vrl/issues/2000
- **Author:** @DoumanAsh
- **Status:** CLOSED (completed)
- **Created:** 2026-10-11T04:00:09Z
- **Closed:** 2026-10-22T19:36:34Z
- **Labels:** good first issue, meta:confirmed, stdlib:to_unix_timestamp

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I encountered issue with my server that vector sends incorrect timestamps:
```
2026-10-11T03:41:41.644560436+00:00 ERROR openobserve_api_ingest::request::logs::ingest: [LOGS:OTLP] Invalid proto: org_id: default failed to decode Protobuf message: LogRecord.time_unix_nano: ScopeLogs.log_records: ResourceLogs.scope_logs: ExportLogsServiceRequest.resource_logs: invalid wire type: LengthDelimited (expected SixtyFourBit)
```

So I decided to investigate because I manually convert my logs into OTLP format:
https://github.com/DoumanAsh/configs/blob/master/vector/vps/syslog_otlp_transform.vrl#L69

At first I thought there could be some error that results in failure of conversion, but when I treid to validate it, vector compiler for VRL says that this function cannot fail (despite what documentation and code indicates):
https://github.com/vectordotdev/vrl/blob/f040d67833601f7af658b1b0f714bd04b9fa4b67/src/stdlib/to_unix_timestamp.rs#L40

Here is error output for VRL compilation:

```
2026-10-11T03:57:25.880978Z ERROR vector::topology::builder: Configuration error. error=Transform "syslog_otlp_transform": 
error[E104]: unnecessary error assignment
   ┌─ :57:18
   │
57 │ time_unix_nanos, err = to_unix_timestamp(real_timestamp, unit: "nanoseconds")
   │ ---------------  ^^^   ------------------------------------------------------ because this expression can't fail
   │ │                │
   │ │                this error assignment is unnecessary
   │ use: time_unix_nanos = to_unix_timestamp(real_timestamp, "nanoseconds")
   │
   = see documentation about error handling at https://errors.vrl.dev/#handling
   = learn more about error code 104 at https://errors.vrl.dev/104
   = see language documentation at https://vrl.dev
   = try your code in the VRL REPL, learn more at https://vrl.dev/examples

error[E701]: call to undefined variable
   ┌─ :58:4
   │
58 │ if err != null {
   │    ^^^
   │    │
   │    undefined variable
   │    did you mean "true"?
   │
   = see language documentation at https://vrl.dev
   = try your code in the VRL REPL, learn more at https://vrl.dev/examples
 internal_log_rate_limit=false
2026-10-11T03:57:25.881651Z ERROR vector::topology::builder: Configuration error. error=Transform "nginx_log_access_otlp_transform": 
error[E104]: unnecessary error assignment
  ┌─ :9:18
  │
9 │ time_unix_nanos, err = to_unix_timestamp(real_timestamp, unit: "nanoseconds")
  │ ---------------  ^^^   ------------------------------------------------------ because this expression can't fail
  │ │                │
  │ │                this error assignment is unnecessary
  │ use: time_unix_nanos = to_unix_timestamp(real_timestamp, "nanoseconds")
  │
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = learn more about error code 104 at https://errors.vrl.dev/104
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

### Configuration

```text

```

### Version

vector 0.59.0 (x86_64-unknown-linux-musl a3231c7 2026-10-06 13:52:51.733983360)

### Debug Output

```text

```

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
