# [#127] Allow specification of multiple timestamp formats to parse_timestamp

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/127)
- **Status**: `OPEN`
- **Author**: [@rabbitstack](https://github.com/rabbitstack)
- **Created At**: `2021-04-09T07:37:53Z`
- **Updated At**: `2026-06-16T13:11:37Z`
- **Comments**: 9
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:parse_timestamp`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/127)

---

## Description

We're experiencing issues with timestamp parsing. Specifically, this is the offending timestamp format:
`07/Apr/2021:23:09:56 +0000`.

 By looking at the Vector [supported](https://github.com/timberio/vector/blob/6ed683e4c44c22493bcb34d97f9e3ab6d3d04a4e/lib/shared/src/conversion.rs#L193) timestamp formats, it doesn't seem to support the above timestamp format. We were wondering whether it would be possible to add it or adjust Vector to permit expanding the timestamp format catalog from the config file?

### Vector Version

```
vector 0.12.1 (v0.12.1 x86_64-unknown-linux-gnu 2021-03-12)
```

### Expected Behavior

`to_timestamp` should produce a valid timestamp.

### Actual Behavior

Apr 07 23:10:05 ip-10-10-25-9.us-west-2.compute.internal vector[3592]: Apr 07 23:10:05.664  WARN transform{component_kind=“transform” component_name=remap-nginx component_type=remap}: vector::internal_events::remap: Mapping failed with event. error=“remap error: function call error: No matching timestamp format found for \“07/Apr/2021:23:09:56 +0000\“” rate_limit_secs=30




