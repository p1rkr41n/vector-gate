# [#462] Converting OpenTelemetry trace_id and span_id to Datadog trace_id

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/462)
- **Status**: `OPEN`
- **Author**: [@hkrutzer](https://github.com/hkrutzer)
- **Created At**: `2023-05-31T14:15:40Z`
- **Updated At**: `2026-06-01T14:17:49Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/462)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

To send logs that have an OpenTelemetry trace_id and space_id to Datadog, and correlate logs with traces, you need to convert the OpenTelemetry trace id to a Datadog trace id as described [here](https://docs.datadoghq.com/tracing/other_telemetry/connect_logs_and_traces/opentelemetry/?tab=nodejs).

However, I can't seem to do this conversion in VRL or lua because neither have longs. It would be great if there was a way to do this conversion in Vector.

### Attempted Solutions

```vrl
if .span_id != null {
  .dd_span_id = to_string(parse_int!(.span_id, 16))
}
if .trace_id != null {
  trace_id_end = slice!(.trace_id, to_int(length(.trace_id) / 2))
  .dd_trace_id = to_string(parse_int!(trace_id_end, 16))
}
```

```json
{
    "level": 30,
    "msg": "request completed",
    "span_id": "985b124a91f072ec",
    "trace_id": "1eda406ed70b61ddee87444efc062b8b"
}
```

```
error[E000]: function call error for "to_string" at (185:224): function call error for "parse_int" at (195:223): could not parse integer: number too large to fit in target type
  ┌─ :6:18
  │
6 │   .dd_trace_id = to_string(parse_int!(trace_id_end, 16))
  │                  ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  │                  │         │
  │                  │         could not parse integer: number too large to fit in target type
  │                  function call error for "parse_int" at (195:223): could not parse integer: number too large to fit in target type
  │
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

### Proposal

Unsure

### References

_No response_

### Version

vector 0.30.0
