# [#1193] parse_aws_alb_log function error failed to get field `client_host`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1193)
- **Status**: `OPEN`
- **Author**: [@mdesouky](https://github.com/mdesouky)
- **Created At**: `2024-12-19T22:36:17Z`
- **Updated At**: `2026-06-16T13:09:44Z`
- **Comments**: 4
- **Labels**: `vrl:stdlib`, `stdlib:parse_aws_alb_log`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1193)

---

## Description

We're trying to ingest AWS alb logs from s3 buckets using the `parse_aws_alb_logs` function but on some logs we get this error message:
```ERROR transform{component_kind="transform" component_id=parse_alb_logs component_type=remap}: vector::internal_events::remap: Mapping failed with event. error="function call error for \"parse_aws_alb_log\" at (13:41): failed to get field `client_host`: Parsing Error: (\"net/nginx-staging-au-1/xxxxxxxxxxxxxxxx xxxxxxxxxxxxxxxx xx.xx.xx.xx:xxxxx xx.xx.xxx.x:xxx 100 6 161 8144 - arn:aws:acm:ap-southeast-2:xxxxxxxxxxxx:certificate/xxxxxxxx-xxxx-xxxx-xxxx-xxxxxxxxxxxx - XXXXX-XXX-XXX000-XXX-XXX000 tlsv12 - xxxxx-xxxxxxx.xxxxxxxx.com - - - 2024-12-19T20:20:28\", TakeWhile1)" error_type="conversion_failed" stage="processing" internal_log_rate_limit=true```

I'm suspecting it's the `TakeWhile1` at the end but not sure
We've deployed vector as a helm chart
Vector version: `0.38.1`
