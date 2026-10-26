# [#1257] Unexpected behaviour of the object_from_array VRL fuction

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1257)
- **Status**: `OPEN`
- **Author**: [@usa4ev](https://github.com/usa4ev)
- **Created At**: `2025-02-04T15:21:41Z`
- **Updated At**: `2026-06-16T13:09:39Z`
- **Comments**: 4
- **Labels**: `vrl:stdlib`, `stdlib:object_from_array`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1257)

---

## Description

### A note for the community


A note for the community

    Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
    If you are interested in working on this issue or have submitted a pull request, please leave a comment

### Problem

VRL function **object_from_array** when used with a single parameter requires unnecessary push to that parameter to work properly. See VRL example in respective section.

What I expect:
```
{
  ...
  "foo": "bar",
  "propstructLen": 1,
  ...
}
```

What I get:
```
{
  ...
  "propstructLen": 0,
  ...
}
```

The function is also not fallible depsite the [doc page](https://vector.dev/docs/reference/vrl/functions/#object_from_array).

### Configuration

```text
config.toml:

[sources.demo_logs]
    type = "demo_logs"
    format = "json"
    lines = [ "line1" ]

[transforms.remap_logs]
	inputs = ["demo_logs"]
	type = "remap"
	file = "/Users/username/test/transform_tj.vrl"

[sinks.print_ok]
    type = "console"
    encoding.codec = "json"
    encoding.json.pretty = true
    inputs = [ "remap_logs" ]


transform_tj.vrl:

proparr = [{"key":"foo", "value":"bar"}]

keyvalarr = []
for_each(proparr) -> |_index, item| {

    PropKey = item.key
    PropValue = item.value

    if is_string(PropKey) {
        keyvalarr = push(keyvalarr, [PropKey, PropValue])
    }
}

# keyvalarr = push(keyvalarr, [null, null])  # <-- when this line is commented out or removed, the next line returns an empty object

propstruct = object_from_array(keyvalarr)
.propstructLen = length(propstruct)
. = merge(., propstruct, deep: false)
```

### Version

vector 0.44.0 (aarch64-apple-darwin 3cdc7c3 2025-01-13 21:26:04.735691656)

### Debug Output

```text
TRACE WHEN object_from_array DOES NOT WORK AS EXPECTED:

2025-02-04T14:55:47.266051Z TRACE vector: Beep.
2025-02-04T14:55:47.266050Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_common::internal_event::bytes_received: Bytes received. byte_size=0 protocol=none
2025-02-04T14:55:47.266149Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector::internal_events::demo_logs: Received one event.
2025-02-04T14:55:47.267182Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_common::internal_event::events_received: Events received. count=1 byte_size=255
2025-02-04T14:55:47.267257Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-04T14:55:47.267273Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=363 output=_default
2025-02-04T14:55:47.267316Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-04T14:55:47.267339Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_core::fanout: Sent item to fanout.
2025-02-04T14:55:47.267368Z TRACE transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector_common::internal_event::events_received: Events received. count=1 byte_size=363
2025-02-04T14:55:47.267614Z TRACE transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-04T14:55:47.267641Z TRACE transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector_core::fanout: Sent item to fanout.
2025-02-04T14:55:47.267651Z TRACE transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=381 output=_default
2025-02-04T14:55:47.267679Z TRACE sink{component_kind="sink" component_id=print_ok component_type=console}: vector_common::internal_event::events_received: Events received. count=1 byte_size=381
2025-02-04T14:55:47.268045Z TRACE sink{component_kind="sink" component_id=print_ok component_type=console}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=379
{
  "host": "localhost",
  "message": "{\"user-identifier\":\"shaneIxD\",\"datetime\":\"04/Feb/2025:17:55:47\",\"method\":\"HEAD\",\"request\":\"/user/booperbot124\",\"protocol\":\"HTTP/2.0\",\"status\":\"300\",\"bytes\":21304,\"referer\":\"https://make.dealer/secret-info/open-sesame\"}",
  "propstructLen": 0,
  "service": "vector",
  "source_type": "demo_logs",
  "timestamp": "2025-02-04T14:55:47.267231Z"
}
2025-02-04T14:55:47.268070Z TRACE sink{component_kind="sink" component_id=print_ok component_type=console}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=439 protocol=console


TRACE WHEN object_from_array WORKS AS EXPECTED:


2025-02-04T14:56:16.860093Z TRACE vector: Beep.
2025-02-04T14:56:16.860093Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_common::internal_event::bytes_received: Bytes received. byte_size=0 protocol=none
2025-02-04T14:56:16.860158Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector::internal_events::demo_logs: Received one event.
2025-02-04T14:56:16.860525Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_common::internal_event::events_received: Events received. count=1 byte_size=243
2025-02-04T14:56:16.860576Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-04T14:56:16.860582Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=351 output=_default
2025-02-04T14:56:16.860993Z DEBUG source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector::topology::builder: Source finished normally.
2025-02-04T14:56:16.861042Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_core::fanout: Processing control message inside of send: None
2025-02-04T14:56:16.861058Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-04T14:56:16.861070Z TRACE source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector_core::fanout: Sent item to fanout.
2025-02-04T14:56:16.861075Z DEBUG source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector::topology::builder: Source pump finished normally.
2025-02-04T14:56:16.861114Z DEBUG source{component_kind="source" component_id=demo_logs component_type=demo_logs}: vector::topology::builder: Source pump supervisor task finished normally.
2025-02-04T14:56:16.861149Z TRACE transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector_common::internal_event::events_received: Events received. count=1 byte_size=351
2025-02-04T14:56:16.861350Z TRACE transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector_core::fanout: Processing control message inside of send: None
2025-02-04T14:56:16.861367Z TRACE transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-04T14:56:16.861374Z TRACE transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector_core::fanout: Sent item to fanout.
2025-02-04T14:56:16.861379Z TRACE transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=381 output=_default
2025-02-04T14:56:16.862045Z DEBUG transform{component_kind="transform" component_id=remap_logs component_type=remap}: vector::topology::builder: Synchronous transform finished normally.
2025-02-04T14:56:16.862093Z TRACE sink{component_kind="sink" component_id=print_ok component_type=console}: vector_common::internal_event::events_received: Events received. count=1 byte_size=381
2025-02-04T14:56:16.862200Z TRACE sink{component_kind="sink" component_id=print_ok component_type=console}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=379
2025-02-04T14:56:16.862208Z TRACE sink{component_kind="sink" component_id=print_ok component_type=console}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=443 protocol=console
{
  "foo": "bar",
  "host": "localhost",
  "message": "{\"user-identifier\":\"KarimMove\",\"datetime\":\"04/Feb/2025:17:56:16\",\"method\":\"HEAD\",\"request\":\"/apps/deploy\",\"protocol\":\"HTTP/2.0\",\"status\":\"307\",\"bytes\":47336,\"referer\":\"https://names.sbs/user/booperbot124\"}",
  "propstructLen": 1,
  "service": "vector",
  "source_type": "demo_logs",
  "timestamp": "2025-02-04T14:56:16.860549Z"
}
2025-02-04T14:56:16.862686Z DEBUG sink{component_kind="sink" component_id=print_ok component_type=console}: vector::topology::builder: Sink finished normally.
```

### Example Data

_No response_

### Additional Context

_No response_

### References

vectordotdev/vector#22294 
