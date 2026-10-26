# Issue #228: Vector does not parse RFC5424 structured data with some escape characters

- **URL:** https://github.com/vectordotdev/vrl/issues/228
- **Author:** @saidsalihefendic
- **Status:** CLOSED (completed)
- **Created:** 2022-09-22T16:45:30Z
- **Closed:** 2023-07-31T16:43:15Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

We've encountered some strange behaviors on VRL function `parse_syslog`, where it discards whole structured data elements if a structured data parameter in structured data contains escape characters (not for all, like `\"`).

When a structured data parameter contains escape character such as `\/`, it then discards whole structured data.

I've tested this also with `vector vrl` and no errors come out, but the structured data with problematic parameter is discarded completely.

### Configuration

```text
[sources.in]
type = "stdin"

[transforms.syslog]
  inputs = ["in"]
  type = "remap"
  source = '''
    . = parse_syslog!(.message)
  '''

[sinks.out]
  inputs = ["syslog"]
  type = "console"
  encoding.codec = "json"
```


### Version

vector 0.24.1 (x86_64-unknown-linux-gnu 8935681 2022-09-12)

### Debug Output

```text
2022-09-22T16:39:43.073219Z  INFO vector::app: Log level is enabled. level="vector=trace,codec=trace,vrl=trace,file_source=trace,tower_limit=trace,rdkafka=trace,buffers=trace,kube=trace"
2022-09-22T16:39:43.073595Z  INFO vector::app: Loading configs. paths=["vector.toml"]
2022-09-22T16:39:43.077649Z DEBUG vector::config::loading: No secret placeholder found, skipping secret resolution.
2022-09-22T16:39:43.082947Z DEBUG vector::topology::builder: Building new source. component=in
2022-09-22T16:39:43.085009Z DEBUG vector::topology::builder: Building new transform. component=syslog
2022-09-22T16:39:43.085829Z  INFO vector::sources::file_descriptors: Capturing stdin.
2022-09-22T16:39:43.086103Z DEBUG vector::topology::builder: Building new sink component=out
2022-09-22T16:39:43.086550Z  INFO vector::topology::running: Running healthchecks.
2022-09-22T16:39:43.086651Z DEBUG vector::topology::running: Connecting changed/added component(s).
2022-09-22T16:39:43.086708Z DEBUG vector::topology::running: Configuring outputs for source. component=in
2022-09-22T16:39:43.086783Z DEBUG vector::topology::running: Configuring output for component. component=in output_id=None
2022-09-22T16:39:43.086858Z DEBUG vector::topology::running: Configuring outputs for transform. component=syslog
2022-09-22T16:39:43.086906Z DEBUG vector::topology::running: Configuring output for component. component=syslog output_id=None
2022-09-22T16:39:43.086964Z DEBUG vector::topology::running: Connecting inputs for transform. component=syslog
2022-09-22T16:39:43.087018Z DEBUG vector::topology::running: Adding component input to fanout. component=syslog fanout_id=in
2022-09-22T16:39:43.087092Z DEBUG vector::topology::running: Connecting inputs for sink. component=out
2022-09-22T16:39:43.087184Z DEBUG vector::topology::running: Adding component input to fanout. component=out fanout_id=syslog
2022-09-22T16:39:43.087233Z  INFO vector::topology::builder: Healthcheck: Passed.
2022-09-22T16:39:43.087385Z DEBUG vector::topology::running: Spawning new source. key=in
2022-09-22T16:39:43.087583Z DEBUG vector::topology::running: Spawning new transform. key=syslog
2022-09-22T16:39:43.087668Z TRACE vector::topology::running: Spawning new sink. key=out
2022-09-22T16:39:43.088123Z  INFO vector: Vector has started. debug="false" version="0.24.1" arch="x86_64" build_id="8935681 2022-09-12"
2022-09-22T16:39:43.088240Z  INFO vector::app: API is disabled, enable by setting `api.enabled` to `true` and use commands like `vector top`.
2022-09-22T16:39:43.089084Z DEBUG source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector::topology::builder: Source pump starting.
2022-09-22T16:39:43.107992Z DEBUG sink{component_kind="sink" component_id=out component_type=console component_name=out}: vector::utilization: utilization=0.000408656499835347
2022-09-22T16:39:43.112136Z TRACE vector: Beep.
<165>1 2022-09-22T13:07:54.228490+00:00 server1 api 12345 - [exampleSD1@66851 field1="example" field2="331" field3="618"][meta@123 field4="123" example_field="\"Hello\" \/World"] 10.0.0.1 - - [22/Sep/2022:13:07:54 +0000] "GET /api/events"2022-09-22T16:39:44.090078Z TRACE vector: Beep.

2022-09-22T16:39:44.484822Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: codecs::decoding::framing::character_delimited: Decoding the frame. bytes_processed=238
2022-09-22T16:39:44.485107Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector::internal_events::common: Bytes received. byte_size=238 protocol=none
2022-09-22T16:39:44.485288Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_common::internal_event::events_received: Events received. count=1 byte_size=1013
2022-09-22T16:39:44.485530Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-09-22T16:39:44.485649Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=749 output=_default
2022-09-22T16:39:44.485774Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "syslog" })
2022-09-22T16:39:44.485918Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-09-22T16:39:44.486026Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_core::fanout: Sent item to fanout.
2022-09-22T16:39:44.486117Z TRACE transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector_common::internal_event::events_received: Events received. count=1 byte_size=749
2022-09-22T16:39:44.486623Z TRACE transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "out" })
2022-09-22T16:39:44.486711Z TRACE transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-09-22T16:39:44.486791Z TRACE transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector_core::fanout: Sent item to fanout.
2022-09-22T16:39:44.486874Z TRACE transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=1212 output=_default
2022-09-22T16:39:44.487023Z TRACE sink{component_kind="sink" component_id=out component_type=console component_name=out}: vector_common::internal_event::events_received: Events received. count=1 byte_size=1188
2022-09-22T16:39:44.487449Z TRACE sink{component_kind="sink" component_id=out component_type=console component_name=out}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=1364
2022-09-22T16:39:44.487525Z TRACE sink{component_kind="sink" component_id=out component_type=console component_name=out}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=292 protocol=console
{"appname":"api","exampleSD1@66851":{"field1":"example","field2":"331","field3":"618"},"facility":"local4","hostname":"server1","message":"10.0.0.1 - - [22/Sep/2022:13:07:54 +0000] \"GET /api/events\"","procid":12345,"severity":"notice","timestamp":"2022-09-22T13:07:54.228490Z","version":1}
2022-09-22T16:39:45.090079Z TRACE vector: Beep.
2022-09-22T16:39:46.089830Z TRACE vector: Beep.
2022-09-22T16:39:47.090178Z TRACE vector: Beep.
2022-09-22T16:39:48.089904Z TRACE vector: Beep.
2022-09-22T16:39:48.089952Z DEBUG sink{component_kind="sink" component_id=out component_type=console component_name=out}: vector::utilization: utilization=0.00014245504246241934
2022-09-22T16:39:49.089432Z TRACE vector: Beep.
<165>1 2022-09-22T13:07:54.228490+00:00 server1 api 12345 - [exampleSD1@66851 field1="example" field2="331" field3="618"][meta@123 field4="123" example_field="\"Hello\" /World"] 10.0.0.1 - - [22/Sep/2022:13:07:54 +0000] "GET /api/events"
2022-09-22T16:39:50.072781Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: codecs::decoding::framing::character_delimited: Decoding the frame. bytes_processed=237
2022-09-22T16:39:50.072900Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector::internal_events::common: Bytes received. byte_size=237 protocol=none
2022-09-22T16:39:50.072954Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_common::internal_event::events_received: Events received. count=1 byte_size=1012
2022-09-22T16:39:50.073041Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-09-22T16:39:50.073081Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=748 output=_default
2022-09-22T16:39:50.073139Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-09-22T16:39:50.073173Z TRACE source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector_core::fanout: Sent item to fanout.
2022-09-22T16:39:50.073215Z DEBUG transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector::utilization: utilization=0.003159884528672663
2022-09-22T16:39:50.073255Z TRACE transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector_common::internal_event::events_received: Events received. count=1 byte_size=748
2022-09-22T16:39:50.073408Z TRACE transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-09-22T16:39:50.073442Z TRACE transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector_core::fanout: Sent item to fanout.
2022-09-22T16:39:50.073474Z TRACE transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=1472 output=_default
2022-09-22T16:39:50.073530Z TRACE sink{component_kind="sink" component_id=out component_type=console component_name=out}: vector_common::internal_event::events_received: Events received. count=1 byte_size=1448
{"appname":"api","exampleSD1@66851":{"field1":"example","field2":"331","field3":"618"},"facility":"local4","hostname":"server1","message":"10.0.0.1 - - [22/Sep/2022:13:07:54 +0000] \"GET /api/events\"","meta@123":{"example_field":"\"Hello\" /World","field4":"123"},"procid":12345,"severity":"notice","timestamp":"2022-09-22T13:07:54.228490Z","version":1}
2022-09-22T16:39:50.073611Z TRACE sink{component_kind="sink" component_id=out component_type=console component_name=out}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=1624
2022-09-22T16:39:50.073651Z TRACE sink{component_kind="sink" component_id=out component_type=console component_name=out}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=355 protocol=console
2022-09-22T16:39:50.089513Z TRACE vector: Beep.
2022-09-22T16:39:51.090044Z TRACE vector: Beep.
2022-09-22T16:39:52.089670Z TRACE vector: Beep.
^C2022-09-22T16:39:52.256719Z  INFO vector: Vector has stopped.
2022-09-22T16:39:52.256889Z  INFO source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector::sources::file_descriptors: Finished sending.
2022-09-22T16:39:52.256940Z DEBUG source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector::topology::builder: Finished.
2022-09-22T16:39:52.256990Z DEBUG source{component_kind="source" component_id=in component_type=stdin component_name=in}: vector::topology::builder: Source pump finished.
2022-09-22T16:39:52.257153Z DEBUG transform{component_kind="transform" component_id=syslog component_type=remap component_name=syslog}: vector::topology::builder: Finished.
2022-09-22T16:39:52.257255Z DEBUG sink{component_kind="sink" component_id=out component_type=console component_name=out}: vector::topology::builder: Finished.
```


### Example Data

<165>1 2022-09-22T13:07:54.228490+00:00 server1 api 12345 - [exampleSD1@66851 field1="example" field2="331" field3="618"][meta@123 field4="123" example_field="\"Hello\" \/World"] 10.0.0.1 - - [22/Sep/2022:13:07:54 +0000] "GET /api/events"
<165>1 2022-09-22T13:07:54.228490+00:00 server1 api 12345 - [exampleSD1@66851 field1="example" field2="331" field3="618"][meta@123 field4="123" example_field="\"Hello\" /World"] 10.0.0.1 - - [22/Sep/2022:13:07:54 +0000] "GET /api/events"


### Additional Context

_No response_

### References

_No response_
