# [#1552] parse_key_value problem when value missing

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1552)
- **Status**: `OPEN`
- **Author**: [@perederyaev](https://github.com/perederyaev)
- **Created At**: `2025-10-29T20:04:48Z`
- **Updated At**: `2026-06-01T14:08:47Z`
- **Comments**: 2
- **Labels**: `stdlib:parse_key_value`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1552)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->

### Problem

When string has only key without value parse_key_value 'eats' next field.
For example, sending output of command `echo -e "field1:\tfield2:2"` to vector's parse_key_value produces 
`{"field1":"field2:2"}` instead of `{"field1": true, "field2":2}`  according accept_standalone_key setting.

### Configuration

```text
sources:
  in:
    type: "stdin"
    decoding:
      codec: "bytes"

transforms:
  transform:
    type: remap
    drop_on_error: true
    inputs:
      - in
    source: |
      .message = parse_key_value!(.message, ":","\t")

sinks:
  out:
    inputs:
      - "transform"
    type: "console"
    encoding:
      codec: "raw_message"
```

### Version

0.50

### Debug Output

```text
2025-10-29T19:58:59.980467Z DEBUG vector::app: Internal log rate limit configured. internal_log_rate_secs=10
2025-10-29T19:58:59.982100Z  INFO vector::app: Log level is enabled. level="trace"
2025-10-29T19:58:59.982741Z DEBUG vector::app: messaged="Building runtime." worker_threads=10
2025-10-29T19:58:59.983615Z TRACE mio::poll: registering event source with poller: token=Token(1), interests=READABLE
2025-10-29T19:58:59.986941Z  INFO vector::app: Loading configs. paths=["vector-parse-key-value.yaml"]
2025-10-29T19:58:59.999193Z DEBUG vector::config::loading: No secret placeholder found, skipping secret resolution.
2025-10-29T19:59:00.020479Z DEBUG vector::topology::builder: Building new source. component=in
2025-10-29T19:59:00.022749Z  INFO vector::sources::file_descriptors: Capturing stdin.
2025-10-29T19:59:00.023046Z DEBUG vector::topology::builder: Building new transform. component=transform
2025-10-29T19:59:00.024526Z DEBUG vector::topology::builder: Building new sink. component=out
2025-10-29T19:59:00.226640Z  INFO vector::topology::running: Running healthchecks.
2025-10-29T19:59:00.226675Z DEBUG vector::topology::running: Connecting changed/added component(s).
2025-10-29T19:59:00.226704Z DEBUG vector::topology::running: Configuring outputs for source. component=in
2025-10-29T19:59:00.226779Z  INFO vector::topology::builder: Healthcheck passed.
2025-10-29T19:59:00.227035Z DEBUG vector::topology::running: Configuring output for component. component=in output_id=None
2025-10-29T19:59:00.227049Z DEBUG vector::topology::running: Configuring outputs for transform. component=transform
2025-10-29T19:59:00.227054Z DEBUG vector::topology::running: Configuring output for component. component=transform output_id=None
2025-10-29T19:59:00.227059Z DEBUG vector::topology::running: Connecting inputs for transform. component=transform
2025-10-29T19:59:00.227066Z DEBUG vector::topology::running: Adding component input to fanout. component=transform fanout_id=in
2025-10-29T19:59:00.227086Z DEBUG vector::topology::running: Connecting inputs for sink. component=out
2025-10-29T19:59:00.227093Z DEBUG vector::topology::running: Adding component input to fanout. component=out fanout_id=transform
2025-10-29T19:59:00.227286Z DEBUG vector::topology::running: Spawning new source. key=in
2025-10-29T19:59:00.227844Z DEBUG vector::topology::running: Spawning new transform. key=transform
2025-10-29T19:59:00.227860Z TRACE vector::topology::running: Spawning new sink. key=out
2025-10-29T19:59:00.228129Z DEBUG transform{component_kind="transform" component_id=transform component_type=remap}: vector::topology::builder: Synchronous transform starting.
2025-10-29T19:59:00.228323Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source pump supervisor starting.
2025-10-29T19:59:00.228309Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source starting.
2025-10-29T19:59:00.228339Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source pump starting.
2025-10-29T19:59:00.228341Z  INFO vector: Vector has started. debug="false" version="0.50.0" arch="aarch64" revision="9053198 2025-09-23 14:18:50.944442940"
2025-10-29T19:59:00.228304Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::topology::builder: Sink starting.
2025-10-29T19:59:00.228318Z DEBUG vector::utilization: utilization=1
2025-10-29T19:59:00.228589Z DEBUG vector::utilization: utilization=1
2025-10-29T19:59:00.228714Z  INFO vector::app: API is disabled, enable by setting `api.enabled` to `true` and use commands like `vector top`.
2025-10-29T19:59:00.228833Z TRACE source{component_kind="source" component_id=in component_type=stdin}: codecs::decoding::framing::character_delimited: Decoding the frame. bytes_processed=16
2025-10-29T19:59:00.229112Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_common::internal_event::bytes_received: Bytes received. byte_size=16 protocol=none
2025-10-29T19:59:00.229447Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_common::internal_event::events_received: Events received. count=1 byte_size=30
2025-10-29T19:59:00.229639Z  INFO vector_common::shutdown: All sources have finished.
2025-10-29T19:59:00.229644Z  INFO vector_common::shutdown: All sources have finished.
2025-10-29T19:59:00.229761Z  INFO vector::app: All sources have finished.
2025-10-29T19:59:00.229771Z  INFO vector: Vector has stopped.
2025-10-29T19:59:00.229869Z TRACE vector: Beep.
2025-10-29T19:59:00.229934Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-10-29T19:59:00.229940Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=119 output=_default
2025-10-29T19:59:00.229948Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::sources::file_descriptors: Finished sending.
2025-10-29T19:59:00.229970Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization start wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-29T19:59:00.230146Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source finished normally.
2025-10-29T19:59:00.230364Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "transform" })
2025-10-29T19:59:00.230376Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_core::fanout: Processing control message inside of send: None
2025-10-29T19:59:00.230385Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-10-29T19:59:00.230389Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_core::fanout: Sent item to fanout.
2025-10-29T19:59:00.230393Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source pump finished normally.
2025-10-29T19:59:00.230534Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source pump supervisor task finished normally.
2025-10-29T19:59:00.230554Z DEBUG transform{component_kind="transform" component_id=transform component_type=remap}: vector::utilization: Couldn't send utilization stop wait message. component_id=ComponentKey { id: "transform" } error="Closed(..)"
2025-10-29T19:59:00.230561Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_common::internal_event::events_received: Events received. count=1 byte_size=119
2025-10-29T19:59:00.230744Z  INFO vector::topology::running: Shutting down... Waiting on running components. remaining_components="transform, out" time_remaining="59 seconds left"
2025-10-29T19:59:00.231953Z DEBUG transform{component_kind="transform" component_id=transform component_type=remap}: vector::utilization: Couldn't send utilization start wait message. component_id=ComponentKey { id: "transform" } error="Closed(..)"
2025-10-29T19:59:00.231965Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "out" })
2025-10-29T19:59:00.231974Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_core::fanout: Processing control message inside of send: None
2025-10-29T19:59:00.231996Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-10-29T19:59:00.232003Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_core::fanout: Sent item to fanout.
2025-10-29T19:59:00.232006Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=122 output=_default
2025-10-29T19:59:00.232015Z DEBUG transform{component_kind="transform" component_id=transform component_type=remap}: vector::topology::builder: Synchronous transform finished normally.
2025-10-29T19:59:00.232581Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization start wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-29T19:59:00.232590Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization stop wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-29T19:59:00.232594Z TRACE sink{component_kind="sink" component_id=out component_type=console}: vector_common::internal_event::events_received: Events received. count=1 byte_size=122
2025-10-29T19:59:00.233086Z TRACE sink{component_kind="sink" component_id=out component_type=console}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=120
2025-10-29T19:59:00.233097Z TRACE sink{component_kind="sink" component_id=out component_type=console}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=22 protocol=console
{"field1":"field2:2"}
2025-10-29T19:59:00.233247Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization start wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-29T19:59:00.233254Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization stop wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-29T19:59:00.233512Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::topology::builder: Sink finished normally.
```

### Example Data

echo -e "field1:\tfield2:2"

### Additional Context

_No response_

### References

_No response_
