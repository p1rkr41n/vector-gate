# Issue #1303: parse_json fails on utf-8 with BOM

- **URL:** https://github.com/vectordotdev/vrl/issues/1303
- **Author:** @MichaelLogutov
- **Status:** CLOSED (completed)
- **Created:** 2025-02-28T13:37:02Z
- **Closed:** 2025-04-08T15:03:42Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

We have windows servers where logs are being written as json into the files (singleline json on mutltiple lines). And those files being written in UTF-8 with BOM. I've noticed that parse_json unable to read the first json (first line) every time there is a new file. Turns out it's because of BOM signature being parsed as json by `parse_json` function and failing.

### Configuration

```text
data_dir = "."

[sources.file]
type = "file"
include = [".\\input.json"]
ignore_checkpoints = true

[transforms.input]
type = "remap"
inputs = ["file"]
drop_on_error = true
reroute_dropped = true
source = '''
    . = parse_json!(.message)
    .type = "test"
'''

[sinks.console]
inputs = ["input"]
type = "console"
encoding.codec = "json"

[sinks.dropped]
inputs = ["input.dropped"]
type = "console"
target = "stderr"
encoding.codec = "json"
```

### Version

vector 0.45.0 (x86_64-pc-windows-msvc 063cabb 2025-02-24 14:52:02.810034614)

### Debug Output

```text
2025-02-28T13:35:44.861584Z DEBUG vector::app: Internal log rate limit configured. internal_log_rate_secs=10
2025-02-28T13:35:44.861711Z  INFO vector::app: Log level is enabled. level="trace"
2025-02-28T13:35:44.861766Z DEBUG vector::app: messaged="Building runtime." worker_threads=16
2025-02-28T13:35:44.873377Z  INFO vector::app: Loading configs. paths=["config.toml"]
2025-02-28T13:35:44.874318Z DEBUG vector::config::loading: No secret placeholder found, skipping secret resolution.
2025-02-28T13:35:44.875807Z DEBUG vector::topology::builder: Building new source. component=file
2025-02-28T13:35:44.876716Z DEBUG vector::topology::builder: Building new transform. component=input
2025-02-28T13:35:44.877174Z DEBUG vector::topology::builder: Building new sink. component=console
2025-02-28T13:35:44.877382Z DEBUG vector::topology::builder: Building new sink. component=dropped
2025-02-28T13:35:45.077585Z  INFO vector::topology::running: Running healthchecks.
2025-02-28T13:35:45.078033Z DEBUG vector::topology::running: Connecting changed/added component(s).
2025-02-28T13:35:45.078333Z DEBUG vector::topology::running: Configuring outputs for source. component=file
2025-02-28T13:35:45.078151Z  INFO vector::topology::builder: Healthcheck passed.
2025-02-28T13:35:45.078651Z  INFO vector::topology::builder: Healthcheck passed.
2025-02-28T13:35:45.078522Z DEBUG vector::topology::running: Configuring output for component. component=file output_id=None
2025-02-28T13:35:45.078879Z DEBUG vector::topology::running: Configuring outputs for transform. component=input
2025-02-28T13:35:45.079046Z DEBUG vector::topology::running: Configuring output for component. component=input output_id=None
2025-02-28T13:35:45.079202Z DEBUG vector::topology::running: Configuring output for component. component=input output_id=Some("dropped")
2025-02-28T13:35:45.079342Z DEBUG vector::topology::running: Connecting inputs for transform. component=input
2025-02-28T13:35:45.079446Z DEBUG vector::topology::running: Adding component input to fanout. component=input fanout_id=file
2025-02-28T13:35:45.079510Z DEBUG vector::topology::running: Connecting inputs for sink. component=dropped
2025-02-28T13:35:45.079558Z DEBUG vector::topology::running: Adding component input to fanout. component=dropped fanout_id=input.dropped
2025-02-28T13:35:45.079605Z DEBUG vector::topology::running: Connecting inputs for sink. component=console
2025-02-28T13:35:45.079649Z DEBUG vector::topology::running: Adding component input to fanout. component=console fanout_id=input
2025-02-28T13:35:45.079731Z DEBUG vector::topology::running: Spawning new source. key=file
2025-02-28T13:35:45.079827Z DEBUG vector::topology::running: Spawning new transform. key=input
2025-02-28T13:35:45.079869Z DEBUG source{component_kind="source" component_id=file component_type=file}: vector::topology::builder: Source pump supervisor starting.
2025-02-28T13:35:45.079874Z DEBUG source{component_kind="source" component_id=file component_type=file}: vector::topology::builder: Source starting.
2025-02-28T13:35:45.079967Z TRACE vector::topology::running: Spawning new sink. key=dropped
2025-02-28T13:35:45.080312Z TRACE vector::topology::running: Spawning new sink. key=console
2025-02-28T13:35:45.080386Z DEBUG sink{component_kind="sink" component_id=dropped component_type=console}: vector::topology::builder: Sink starting.
2025-02-28T13:35:45.080111Z DEBUG source{component_kind="source" component_id=file component_type=file}: vector::topology::builder: Source pump starting.
2025-02-28T13:35:45.080282Z  INFO source{component_kind="source" component_id=file component_type=file}: vector::sources::file: Starting file server. include=[".\\input.json"] exclude=[]
2025-02-28T13:35:45.080001Z DEBUG transform{component_kind="transform" component_id=input component_type=remap}: vector::topology::builder: Synchronous transform starting.
2025-02-28T13:35:45.080421Z DEBUG sink{component_kind="sink" component_id=console component_type=console}: vector::topology::builder: Sink starting.
2025-02-28T13:35:45.080456Z  INFO vector: Vector has started. debug="false" version="0.45.0" arch="x86_64" revision="063cabb 2025-02-24 14:52:02.810034614"
2025-02-28T13:35:45.081061Z  INFO vector::app: API is disabled, enable by setting `api.enabled` to `true` and use commands like `vector top`.
2025-02-28T13:35:45.081939Z  INFO source{component_kind="source" component_id=file component_type=file}:file_server: file_source::checkpointer: Loaded checkpoint data.
2025-02-28T13:35:45.082300Z  INFO source{component_kind="source" component_id=file component_type=file}:file_server: vector::internal_events::file::source: Found new file to watch. file=input.json
2025-02-28T13:35:45.082658Z TRACE source{component_kind="source" component_id=file component_type=file}:file_server: file_source::file_server: Continue watching file. path="input.json"
2025-02-28T13:35:45.082752Z TRACE source{component_kind="source" component_id=file component_type=file}:file_server: file_source::file_server: Read bytes. path="input.json" bytes=15
2025-02-28T13:35:45.082810Z TRACE source{component_kind="source" component_id=file component_type=file}:file_server: file_source::file_server: Read bytes. path="input.json" bytes=12
2025-02-28T13:35:45.082913Z TRACE source{component_kind="source" component_id=file component_type=file}: vector::internal_events::file::source: Bytes received. byte_size=15 protocol="file" file=input.json
2025-02-28T13:35:45.082994Z TRACE source{component_kind="source" component_id=file component_type=file}: vector::internal_events::file::source: Events received. count=1 byte_size=137 file=input.json
2025-02-28T13:35:45.083060Z TRACE source{component_kind="source" component_id=file component_type=file}: vector::internal_events::file::source: Bytes received. byte_size=12 protocol="file" file=input.json
2025-02-28T13:35:45.083114Z TRACE source{component_kind="source" component_id=file component_type=file}: vector::internal_events::file::source: Events received. count=1 byte_size=134 file=input.json
2025-02-28T13:35:45.083182Z TRACE source{component_kind="source" component_id=file component_type=file}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-28T13:35:45.083227Z TRACE source{component_kind="source" component_id=file component_type=file}: vector_common::internal_event::events_sent: Events sent. count=2 byte_size=274 output=_default
2025-02-28T13:35:45.083288Z TRACE source{component_kind="source" component_id=file component_type=file}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "input" })
2025-02-28T13:35:45.083358Z TRACE source{component_kind="source" component_id=file component_type=file}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-28T13:35:45.083436Z TRACE vector: Beep.
2025-02-28T13:35:45.083436Z TRACE source{component_kind="source" component_id=file component_type=file}: vector_core::fanout: Sent item to fanout.
2025-02-28T13:35:45.083417Z DEBUG sink{component_kind="sink" component_id=console component_type=console}: vector::utilization: utilization=0.012428021044782356
2025-02-28T13:35:45.083417Z DEBUG sink{component_kind="sink" component_id=dropped component_type=console}: vector::utilization: utilization=0.011884608740715175
2025-02-28T13:35:45.083570Z TRACE transform{component_kind="transform" component_id=input component_type=remap}: vector_common::internal_event::events_received: Events received. count=2 byte_size=274
2025-02-28T13:35:45.084004Z TRACE transform{component_kind="transform" component_id=input component_type=remap}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "console" })
2025-02-28T13:35:45.084088Z TRACE transform{component_kind="transform" component_id=input component_type=remap}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-28T13:35:45.084137Z TRACE transform{component_kind="transform" component_id=input component_type=remap}: vector_core::fanout: Sent item to fanout.
2025-02-28T13:35:45.084182Z TRACE transform{component_kind="transform" component_id=input component_type=remap}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=27 output=_default
2025-02-28T13:35:45.084236Z TRACE transform{component_kind="transform" component_id=input component_type=remap}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "dropped" })
2025-02-28T13:35:45.084291Z TRACE transform{component_kind="transform" component_id=input component_type=remap}: vector_buffers::topology::channel::limited_queue: Sent item.
2025-02-28T13:35:45.084341Z TRACE transform{component_kind="transform" component_id=input component_type=remap}: vector_core::fanout: Sent item to fanout.
2025-02-28T13:35:45.084387Z TRACE transform{component_kind="transform" component_id=input component_type=remap}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=374 output=dropped
2025-02-28T13:35:45.084305Z TRACE sink{component_kind="sink" component_id=console component_type=console}: vector_common::internal_event::events_received: Events received. count=1 byte_size=27
2025-02-28T13:35:45.084447Z TRACE sink{component_kind="sink" component_id=dropped component_type=console}: vector_common::internal_event::events_received: Events received. count=1 byte_size=374
2025-02-28T13:35:45.085780Z TRACE sink{component_kind="sink" component_id=console component_type=console}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=25
2025-02-28T13:35:45.085842Z TRACE sink{component_kind="sink" component_id=console component_type=console}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=26 protocol=console
2025-02-28T13:35:45.086323Z TRACE sink{component_kind="sink" component_id=dropped component_type=console}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=372
{"type":"test","value":2}
2025-02-28T13:35:45.086422Z TRACE sink{component_kind="sink" component_id=dropped component_type=console}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=378 protocol=console
{"file":"input.json","host":"laptop","message":"﻿{\"value\":1}\r","metadata":{"dropped":{"component_id":"input","component_kind":"transform","component_type":"remap","message":"function call error for \"parse_json\" at (8:29): unable to parse json: expected value at line 1 column 1","reason":"error"}},"source_type":"file","timestamp":"2025-02-28T13:35:45.082983600Z"}
2025-02-28T13:35:46.087665Z TRACE vector: Beep.
2025-02-28T13:35:46.089833Z DEBUG vector::internal_events::file::source: Files checkpointed. count=2 duration_ms=2
2025-02-28T13:35:46.212016Z DEBUG source{component_kind="source" component_id=file component_type=file}:file_server: file_source::file_server: event_throughput=2.000/sec bytes_throughput=27.000/sec ratios={"discovery": 0.00029011472, "other": 0.00011774568, "reading": 0.00022221178, "sending": 4.957713e-5, "sleeping": 0.99932045}
2025-02-28T13:35:46.212616Z TRACE source{component_kind="source" component_id=file component_type=file}:file_server: file_source::file_server: Continue watching file. path="input.json"
2025-02-28T13:35:47.091189Z TRACE vector: Beep.
2025-02-28T13:35:47.091212Z DEBUG vector::internal_events::file::source: Files checkpointed. count=2 duration_ms=0
2025-02-28T13:35:47.244369Z DEBUG source{component_kind="source" component_id=file component_type=file}:file_server: file_source::file_server: event_throughput=1.000/sec bytes_throughput=13.000/sec ratios={"discovery": 0.0004166146, "other": 0.00022206802, "reading": 0.00012460972, "sending": 2.8909086e-5, "sleeping": 0.99920785}
2025-02-28T13:35:47.244866Z TRACE source{component_kind="source" component_id=file component_type=file}:file_server: file_source::file_server: Continue watching file. path="input.json"
2025-02-28T13:35:48.097708Z TRACE vector: Beep.
2025-02-28T13:35:48.097806Z DEBUG vector::internal_events::file::source: Files checkpointed. count=2 duration_ms=0
2025-02-28T13:35:49.088030Z TRACE vector: Beep.
2025-02-28T13:35:49.103285Z DEBUG vector::internal_events::file::source: Files checkpointed. count=2 duration_ms=0
2025-02-28T13:35:49.303801Z DEBUG source{component_kind="source" component_id=file component_type=file}:file_server: file_source::file_server: event_throughput=0.000/sec bytes_throughput=6.000/sec ratios={"discovery": 0.00029345925, "other": 0.00017608028, "reading": 6.483677e-5, "sending": 1.6013759e-5, "sleeping": 0.9994497}
2025-02-28T13:35:49.304300Z TRACE source{component_kind="source" component_id=file component_type=file}:file_server: file_source::file_server: Continue watching file. path="input.json"
2025-02-28T13:35:49.454523Z  INFO vector: Vector has stopped.
2025-02-28T13:35:49.454844Z  INFO vector::topology::running: Shutting down... Waiting on running components. remaining_components="input, file, console, dropped" time_remaining="59 seconds left"
2025-02-28T13:35:49.454997Z DEBUG source{component_kind="source" component_id=file component_type=file}: vector::topology::builder: Source finished normally.
2025-02-28T13:35:49.454870Z DEBUG vector::sources::file: Finished sending.
2025-02-28T13:35:49.455269Z DEBUG source{component_kind="source" component_id=file component_type=file}: vector::topology::builder: Source pump finished normally.
2025-02-28T13:35:49.455390Z DEBUG source{component_kind="source" component_id=file component_type=file}: vector::topology::builder: Source pump supervisor task finished normally.
2025-02-28T13:35:49.455448Z DEBUG transform{component_kind="transform" component_id=input component_type=remap}: vector::topology::builder: Synchronous transform finished normally.
2025-02-28T13:35:49.455476Z DEBUG sink{component_kind="sink" component_id=console component_type=console}: vector::topology::builder: Sink finished normally.
2025-02-28T13:35:49.455556Z DEBUG sink{component_kind="sink" component_id=dropped component_type=console}: vector::topology::builder: Sink finished normally.
```

### Example Data

[input.json](https://github.com/user-attachments/files/19028140/input.json)

### Additional Context
Current workaround - replace VRL remap with this:
```
source = '''
    json, err = parse_json(.message)
    if err != null {
        json = parse_json!(slice!(.message, 3))
    }
    . = json
    .type = "test"
'''
```

### References

_No response_
