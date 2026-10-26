# [#215] CEF parser failed to parse a log message

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/215)
- **Status**: `OPEN`
- **Author**: [@v8v5v](https://github.com/v8v5v)
- **Created At**: `2023-05-03T11:12:13Z`
- **Updated At**: `2026-06-01T14:06:40Z`
- **Comments**: 4
- **Labels**: `vrl:stdlib`, `stdlib:parse_cef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/215)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I was trying to parse Incapsula CEF log which look like:
```
CEF:0|Incapsula|SIEMintegration|1|1|Illegal Resource Access|3| fileid=3412341160002518171
```
(more examples could be found [here](https://docs.imperva.com/bundle/cloud-application-security/page/more/example-logs.htm#logEx1))

The CEF parser could not parse this log message, probably because the last `|` sign has the trailing space. 
After I manually fixed the log by removing the space between the last `|` and the following `fileid`, then it was parsed without any issue.
```
CEF:0|Incapsula|SIEMintegration|1|1|Illegal Resource Access|3|fileid=3412341160002518171
```
It would be great to modify the CEF Parser and make it parse maybe non-standard logs which sometimes happen to exist in real life..



### Configuration

```text
[sources.my_file_source]
type = "file"
include = ["/tmp/test.log"]
ignore_not_found = true

[transforms.my_cef_parser]
type = "remap"
inputs = ["my_file_source"]
source = '''
# Parse CEF message
. = parse_cef!(.message)
'''

[sinks.my_console_sink]
type = "console"
inputs = ["my_cef_parser"]
encoding.codec = "json"
# Pretty-print JSON output
encoding.indent = 2
```


### Version

vector 0.29.1 (x86_64-unknown-linux-gnu 74ae15e 2023-04-20 14:50:42.739094536)

### Debug Output

```text
2023-05-03T11:09:29.118796Z DEBUG vector::app: Internal log rate limit configured. internal_log_rate_secs=10
2023-05-03T11:09:29.118858Z  INFO vector::app: Log level is enabled. level="vector=trace,codec=trace,vrl=trace,file_source=trace,tower_limit=trace,rdkafka=trace,buffers=trace,lapin=trace,kube=trace"
2023-05-03T11:09:29.121516Z  INFO vector::app: Loading configs. paths=["/etc/vector/vector.toml"]
2023-05-03T11:09:29.122083Z DEBUG vector::config::loading: No secret placeholder found, skipping secret resolution.
2023-05-03T11:09:29.123590Z DEBUG vector::topology::builder: Building new source. component=my_file_source
2023-05-03T11:09:29.123916Z DEBUG vector::topology::builder: Building new transform. component=my_cef_parser
2023-05-03T11:09:29.124251Z DEBUG vector::topology::builder: Building new sink. component=my_console_sink
2023-05-03T11:09:29.124457Z  INFO vector::topology::running: Running healthchecks.
2023-05-03T11:09:29.124477Z DEBUG vector::topology::running: Connecting changed/added component(s).
2023-05-03T11:09:29.124498Z DEBUG vector::topology::running: Configuring outputs for source. component=my_file_source
2023-05-03T11:09:29.124515Z DEBUG vector::topology::running: Configuring output for component. component=my_file_source output_id=None
2023-05-03T11:09:29.124526Z DEBUG vector::topology::running: Configuring outputs for transform. component=my_cef_parser
2023-05-03T11:09:29.124534Z DEBUG vector::topology::running: Configuring output for component. component=my_cef_parser output_id=None
2023-05-03T11:09:29.124545Z DEBUG vector::topology::running: Connecting inputs for transform. component=my_cef_parser
2023-05-03T11:09:29.124558Z DEBUG vector::topology::running: Adding component input to fanout. component=my_cef_parser fanout_id=my_file_source
2023-05-03T11:09:29.124574Z DEBUG vector::topology::running: Connecting inputs for sink. component=my_console_sink
2023-05-03T11:09:29.124584Z DEBUG vector::topology::running: Adding component input to fanout. component=my_console_sink fanout_id=my_cef_parser
2023-05-03T11:09:29.124629Z DEBUG vector::topology::running: Spawning new source. key=my_file_source
2023-05-03T11:09:29.124665Z DEBUG vector::topology::running: Registered new allocation group. component_kind="source" component_type="file" component_id="my_file_source" group_id="2"
2023-05-03T11:09:29.124688Z DEBUG vector::topology::running: Spawning new transform. key=my_cef_parser
2023-05-03T11:09:29.124711Z DEBUG vector::topology::running: Registered new allocation group. component_kind="transform" component_type="remap" component_id="my_cef_parser" group_id="3"
2023-05-03T11:09:29.124732Z TRACE vector::topology::running: Spawning new sink. key=my_console_sink
2023-05-03T11:09:29.124758Z DEBUG vector::topology::running: Registered new allocation group. component_kind="sink" component_type="console" component_id="my_console_sink" group_id="4"
2023-05-03T11:09:29.124818Z  INFO vector: Vector has started. debug="false" version="0.29.1" arch="x86_64" revision="74ae15e 2023-04-20 14:50:42.739094536"
2023-05-03T11:09:29.124845Z  INFO vector::app: API is disabled, enable by setting `api.enabled` to `true` and use commands like `vector top`.
2023-05-03T11:09:29.125098Z  INFO vector::topology::builder: Healthcheck passed.
2023-05-03T11:09:29.125132Z DEBUG source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector::topology::builder: Source starting.
2023-05-03T11:09:29.125187Z  INFO source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector::sources::file: Starting file server. include=["/tmp/test.log"] exclude=[]
2023-05-03T11:09:29.125973Z DEBUG source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector::topology::builder: Source pump supervisor starting.
2023-05-03T11:09:29.126111Z DEBUG source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector::topology::builder: Source pump starting.
2023-05-03T11:09:29.126136Z DEBUG transform{component_kind="transform" component_id=my_cef_parser component_type=remap component_name=my_cef_parser}: vector::topology::builder: Synchronous transform starting.
2023-05-03T11:09:29.126154Z DEBUG sink{component_kind="sink" component_id=my_console_sink component_type=console component_name=my_console_sink}: vector::topology::builder: Sink starting.
2023-05-03T11:09:29.127348Z TRACE vector: Beep.
2023-05-03T11:09:29.127369Z DEBUG sink{component_kind="sink" component_id=my_console_sink component_type=console component_name=my_console_sink}: vector::utilization: utilization=0.05264400984195372
2023-05-03T11:09:29.128240Z  INFO source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}:file_server: file_source::checkpointer: Attempting to read legacy checkpoint files.
2023-05-03T11:09:29.132531Z  INFO source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}:file_server: vector::internal_events::file::source: Found new file to watch. file=/tmp/test.log
2023-05-03T11:09:29.132620Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}:file_server: file_source::file_server: Continue watching file. path="/tmp/test.log"
2023-05-03T11:09:29.132662Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}:file_server: file_source::file_server: Read bytes. path="/tmp/test.log" bytes=72
2023-05-03T11:09:29.132846Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector::internal_events::file::source: Bytes received. byte_size=72 protocol="file" file=/tmp/test.log
2023-05-03T11:09:29.132900Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector::internal_events::file::source: Events received. count=1 byte_size=72 file=/tmp/test.log
2023-05-03T11:09:29.132989Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector_buffers::topology::channel::limited_queue: Sent item.
2023-05-03T11:09:29.133009Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=203 output=_default
2023-05-03T11:09:29.133032Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "my_cef_parser" })
2023-05-03T11:09:29.138909Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector_buffers::topology::channel::limited_queue: Sent item.
2023-05-03T11:09:29.138931Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}: vector_core::fanout: Sent item to fanout.
2023-05-03T11:09:29.138952Z TRACE transform{component_kind="transform" component_id=my_cef_parser component_type=remap component_name=my_cef_parser}: vector_common::internal_event::events_received: Events received. count=1 byte_size=203
2023-05-03T11:09:29.139055Z ERROR transform{component_kind="transform" component_id=my_cef_parser component_type=remap component_name=my_cef_parser}: vector::internal_events::remap: Mapping failed with event. error="function call error for \"parse_cef\" at (24:44): Could not parse whole line successfully" error_type="conversion_failed" stage="processing" internal_log_rate_limit=true
2023-05-03T11:09:29.139133Z TRACE transform{component_kind="transform" component_id=my_cef_parser component_type=remap component_name=my_cef_parser}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "my_console_sink" })
2023-05-03T11:09:29.139147Z TRACE transform{component_kind="transform" component_id=my_cef_parser component_type=remap component_name=my_cef_parser}: vector_buffers::topology::channel::limited_queue: Sent item.
2023-05-03T11:09:29.139154Z TRACE transform{component_kind="transform" component_id=my_cef_parser component_type=remap component_name=my_cef_parser}: vector_core::fanout: Sent item to fanout.
2023-05-03T11:09:29.139161Z TRACE transform{component_kind="transform" component_id=my_cef_parser component_type=remap component_name=my_cef_parser}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=203 output=_default
2023-05-03T11:09:29.139176Z TRACE sink{component_kind="sink" component_id=my_console_sink component_type=console component_name=my_console_sink}: vector_common::internal_event::events_received: Events received. count=1 byte_size=203
2023-05-03T11:09:29.139898Z TRACE sink{component_kind="sink" component_id=my_console_sink component_type=console component_name=my_console_sink}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=201
2023-05-03T11:09:29.139934Z TRACE sink{component_kind="sink" component_id=my_console_sink component_type=console component_name=my_console_sink}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=202 protocol=console
{"file":"/tmp/test.log","host":"X","message":"CEF:0|Incapsula|SIEMintegration|1|1|Normal|0| fileId=1276000830014346377","source_type":"file","timestamp":"2023-05-03T11:09:29.132935551Z"}
2023-05-03T11:09:30.127950Z TRACE vector: Beep.
2023-05-03T11:09:30.139153Z DEBUG vector::internal_events::file::source: Files checkpointed. count=1 duration_ms=4
2023-05-03T11:09:30.165563Z DEBUG source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}:file_server: file_source::file_server: event_throughput=1.000/sec bytes_throughput=72.000/sec ratios={"discovery": 5.7603964e-5, "other": 0.00015309395, "reading": 0.000107883396, "sending": 0.00015582104, "sleeping": 0.99952674}
2023-05-03T11:09:30.165692Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}:file_server: file_source::file_server: Continue watching file. path="/tmp/test.log"
2023-05-03T11:09:31.127300Z TRACE vector: Beep.
2023-05-03T11:09:31.140503Z DEBUG vector::internal_events::file::source: Files checkpointed. count=1 duration_ms=0
2023-05-03T11:09:31.190994Z DEBUG source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}:file_server: file_source::file_server: event_throughput=0.000/sec bytes_throughput=36.000/sec ratios={"discovery": 6.269027e-5, "other": 0.00013159559, "reading": 5.6451896e-5, "sending": 8.3148494e-5, "sleeping": 0.99966663}
2023-05-03T11:09:31.191126Z TRACE source{component_kind="source" component_id=my_file_source component_type=file component_name=my_file_source}:file_server: file_source::file_server: Continue watching file. path="/tmp/test.log"
^C2023-05-03T11:09:31.687408Z  INFO vector::signal: Signal received. signal="SIGINT"
2023-05-03T11:09:31.687510Z  INFO vector: Vector has stopped
```


### Example Data

CEF:0|Incapsula|SIEMintegration|1|1|Illegal Resource Access|3| fileid=3412341160002518171

### Additional Context

_No response_

### References

_No response_
