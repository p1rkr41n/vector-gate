# [#1548] parse_key_value problem when value missing

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1548)
- **Status**: `OPEN`
- **Author**: [@perederyaev](https://github.com/perederyaev)
- **Created At**: `2025-10-31T16:30:10Z`
- **Updated At**: `2026-06-01T14:08:48Z`
- **Comments**: 0
- **Labels**: `stdlib:parse_key_value`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1548)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

When string has only key without value parse_key_value 'eats' next field.
For example, sending output of command echo -e "field1:\tfield2:2" to vector's parse_key_value produces
`{"field1":"field2:2"}`
instead of 
`{"field1": true, "field2": 2} `
according accept_standalone_key.

### VRL Program

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
      .message = parse_key_value!(.message, 	field_delimiter: "\t", key_value_delimiter: ":", accept_standalone_key: true)


sinks:
  out:
    inputs:
      - "transform"
    type: "console"
    encoding:
      codec: "raw_message"
```

### VRL and/or Vector Version

0.50

### Debug Output

```text
2025-10-31T16:28:37.838535Z DEBUG vector::app: Internal log rate limit configured. internal_log_rate_secs=10
2025-10-31T16:28:37.839749Z  INFO vector::app: Log level is enabled. level="trace"
2025-10-31T16:28:37.840191Z DEBUG vector::app: messaged="Building runtime." worker_threads=10
2025-10-31T16:28:37.840971Z TRACE mio::poll: registering event source with poller: token=Token(1), interests=READABLE
2025-10-31T16:28:37.847193Z  INFO vector::app: Loading configs. paths=["vector-parse-key-value.yaml"]
2025-10-31T16:28:37.855626Z DEBUG vector::config::loading: No secret placeholder found, skipping secret resolution.
2025-10-31T16:28:37.873969Z DEBUG vector::topology::builder: Building new source. component=in
2025-10-31T16:28:37.876186Z  INFO vector::sources::file_descriptors: Capturing stdin.
2025-10-31T16:28:37.876288Z DEBUG vector::topology::builder: Building new transform. component=transform
2025-10-31T16:28:37.877364Z DEBUG vector::topology::builder: Building new sink. component=out
2025-10-31T16:28:38.078178Z  INFO vector::topology::running: Running healthchecks.
2025-10-31T16:28:38.078284Z DEBUG vector::topology::running: Connecting changed/added component(s).
2025-10-31T16:28:38.078460Z  INFO vector::topology::builder: Healthcheck passed.
2025-10-31T16:28:38.079155Z DEBUG vector::topology::running: Configuring outputs for source. component=in
2025-10-31T16:28:38.079768Z DEBUG vector::topology::running: Configuring output for component. component=in output_id=None
2025-10-31T16:28:38.079786Z DEBUG vector::topology::running: Configuring outputs for transform. component=transform
2025-10-31T16:28:38.079791Z DEBUG vector::topology::running: Configuring output for component. component=transform output_id=None
2025-10-31T16:28:38.079797Z DEBUG vector::topology::running: Connecting inputs for transform. component=transform
2025-10-31T16:28:38.079809Z DEBUG vector::topology::running: Adding component input to fanout. component=transform fanout_id=in
2025-10-31T16:28:38.080069Z DEBUG vector::topology::running: Connecting inputs for sink. component=out
2025-10-31T16:28:38.080147Z DEBUG vector::topology::running: Adding component input to fanout. component=out fanout_id=transform
2025-10-31T16:28:38.080197Z DEBUG vector::topology::running: Spawning new source. key=in
2025-10-31T16:28:38.080496Z DEBUG vector::topology::running: Spawning new transform. key=transform
2025-10-31T16:28:38.080511Z TRACE vector::topology::running: Spawning new sink. key=out
2025-10-31T16:28:38.080867Z  INFO vector: Vector has started. debug="false" version="0.50.0" arch="aarch64" revision="9053198 2025-09-23 14:18:50.944442940"
2025-10-31T16:28:38.080889Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source pump supervisor starting.
2025-10-31T16:28:38.081219Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source pump starting.
2025-10-31T16:28:38.080668Z DEBUG vector::utilization: utilization=1
2025-10-31T16:28:38.081242Z DEBUG vector::utilization: utilization=1
2025-10-31T16:28:38.080689Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source starting.
2025-10-31T16:28:38.080812Z DEBUG transform{component_kind="transform" component_id=transform component_type=remap}: vector::topology::builder: Synchronous transform starting.
2025-10-31T16:28:38.080666Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::topology::builder: Sink starting.
2025-10-31T16:28:38.081196Z  INFO vector::app: API is disabled, enable by setting `api.enabled` to `true` and use commands like `vector top`.
2025-10-31T16:28:38.082548Z TRACE vector: Beep.
2025-10-31T16:28:38.082645Z TRACE source{component_kind="source" component_id=in component_type=stdin}: codecs::decoding::framing::character_delimited: Decoding the frame. bytes_processed=16
2025-10-31T16:28:38.082927Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_common::internal_event::bytes_received: Bytes received. byte_size=16 protocol=none
2025-10-31T16:28:38.083278Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_common::internal_event::events_received: Events received. count=1 byte_size=30
2025-10-31T16:28:38.084381Z  INFO vector_common::shutdown: All sources have finished.
2025-10-31T16:28:38.084447Z  INFO vector_common::shutdown: All sources have finished.
2025-10-31T16:28:38.084481Z  INFO vector::app: All sources have finished.
2025-10-31T16:28:38.084493Z  INFO vector: Vector has stopped.
2025-10-31T16:28:38.084802Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-10-31T16:28:38.084821Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=119 output=_default
2025-10-31T16:28:38.084834Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::sources::file_descriptors: Finished sending.
2025-10-31T16:28:38.084798Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization start wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-31T16:28:38.085082Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source finished normally.
2025-10-31T16:28:38.085133Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "transform" })
2025-10-31T16:28:38.085153Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_core::fanout: Processing control message inside of send: None
2025-10-31T16:28:38.085165Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-10-31T16:28:38.085171Z TRACE source{component_kind="source" component_id=in component_type=stdin}: vector_core::fanout: Sent item to fanout.
2025-10-31T16:28:38.085174Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source pump finished normally.
2025-10-31T16:28:38.085746Z DEBUG source{component_kind="source" component_id=in component_type=stdin}: vector::topology::builder: Source pump supervisor task finished normally.
2025-10-31T16:28:38.085779Z DEBUG transform{component_kind="transform" component_id=transform component_type=remap}: vector::utilization: Couldn't send utilization stop wait message. component_id=ComponentKey { id: "transform" } error="Closed(..)"
2025-10-31T16:28:38.085787Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_common::internal_event::events_received: Events received. count=1 byte_size=119
2025-10-31T16:28:38.085795Z  INFO vector::topology::running: Shutting down... Waiting on running components. remaining_components="out, in, transform" time_remaining="59 seconds left"
2025-10-31T16:28:38.087881Z DEBUG transform{component_kind="transform" component_id=transform component_type=remap}: vector::utilization: Couldn't send utilization start wait message. component_id=ComponentKey { id: "transform" } error="Closed(..)"
2025-10-31T16:28:38.087908Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "out" })
2025-10-31T16:28:38.087921Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_core::fanout: Processing control message inside of send: None
2025-10-31T16:28:38.087948Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-10-31T16:28:38.087954Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_core::fanout: Sent item to fanout.
2025-10-31T16:28:38.087958Z TRACE transform{component_kind="transform" component_id=transform component_type=remap}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=122 output=_default
2025-10-31T16:28:38.087978Z DEBUG transform{component_kind="transform" component_id=transform component_type=remap}: vector::topology::builder: Synchronous transform finished normally.
2025-10-31T16:28:38.088198Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization start wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-31T16:28:38.088213Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization stop wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-31T16:28:38.088218Z TRACE sink{component_kind="sink" component_id=out component_type=console}: vector_common::internal_event::events_received: Events received. count=1 byte_size=122
2025-10-31T16:28:38.089162Z TRACE sink{component_kind="sink" component_id=out component_type=console}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=120
2025-10-31T16:28:38.089176Z TRACE sink{component_kind="sink" component_id=out component_type=console}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=22 protocol=console
2025-10-31T16:28:38.089200Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization start wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-31T16:28:38.089207Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::utilization: Couldn't send utilization stop wait message. component_id=ComponentKey { id: "out" } error="Closed(..)"
2025-10-31T16:28:38.089237Z DEBUG sink{component_kind="sink" component_id=out component_type=console}: vector::topology::builder: Sink finished normally.
{"field1":"field2:2"}
```

### Example

echo -e "field1:\tfield2:2"

### Additional Context

_No response_

### References

_No response_
