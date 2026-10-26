# Issue #227: AWS VPC FLOW logs fields missing

- **URL:** https://github.com/vectordotdev/vrl/issues/227
- **Author:** @voyc-geoffrey
- **Status:** CLOSED (completed)
- **Created:** 2022-11-17T13:19:52Z
- **Closed:** 2023-09-25T22:04:21Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I am trying to filter custom AWS VPC Flow logs. They are very verbose and use 21 of the 29 [available fields](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-logs-fields). 

I tried using `. = parse_aws_vpc_flow_log!(string!(.message), format: "log_status az_id instance_id vpc_id subnet_id start end flow_direction action pkt_src_aws_service pkt_dst_aws_service srcaddr pkt_srcaddr srcport dstaddr dstport pkt_dstaddr protocol type packets bytes")` however, pkt_src_aws_service, pkt_dst_aws_service and flow_direction would not resolve as it looks like it was never catered for?

This would ultimately fail to parse.


### Configuration

```text
Vector config:
===============================================
[sources.in]

type = "file"
ignore_older_secs = 6000
include = [ "/var/log/test.log" ]
read_from = "beginning"

[transforms.flow_logs]

type = "remap"
inputs = ["in"]
drop_on_error = false
source = '''
. = parse_aws_vpc_flow_log!(string!(.message), format: "log_status az_id instance_id vpc_id subnet_id start end action srcaddr pkt_srcaddr srcport dstaddr dstport pkt_dstaddr protocol type packets bytes")
'''

[sinks.my_sink_id]
type = "console"
inputs = [ "flow_logs" ]
target = "stdout"

  [sinks.my_sink_id.encoding]
  codec = "json"
```


### Version

vector 0.25.1

### Debug Output

```text
2022-11-17T13:17:16.128909Z  INFO vector::app: Internal log rate limit configured. internal_log_rate_secs=10
2022-11-17T13:17:16.128986Z  INFO vector::app: Log level is enabled. level="vector=trace,codec=trace,vrl=trace,file_source=trace,tower_limit=trace,rdkafka=trace,buffers=trace,lapin=trace,kube=trace"
2022-11-17T13:17:16.129031Z  INFO vector::app: Loading configs. paths=["vector.toml"]
2022-11-17T13:17:16.129530Z DEBUG vector::config::loading: No secret placeholder found, skipping secret resolution.
2022-11-17T13:17:16.130286Z DEBUG vector::topology::builder: Building new source. component=in
2022-11-17T13:17:16.130722Z DEBUG vector::topology::builder: Building new transform. component=flow_logs
2022-11-17T13:17:16.131031Z DEBUG vector::topology::builder: Building new sink. component=my_sink_id
2022-11-17T13:17:16.131108Z  INFO vector::topology::running: Running healthchecks.
2022-11-17T13:17:16.131144Z DEBUG vector::topology::running: Connecting changed/added component(s).
2022-11-17T13:17:16.131170Z DEBUG vector::topology::running: Configuring outputs for source. component=in
2022-11-17T13:17:16.131202Z DEBUG vector::topology::running: Configuring output for component. component=in output_id=None
2022-11-17T13:17:16.131212Z DEBUG vector::topology::running: Configuring outputs for transform. component=flow_logs
2022-11-17T13:17:16.131217Z DEBUG vector::topology::running: Configuring output for component. component=flow_logs output_id=None
2022-11-17T13:17:16.131221Z DEBUG vector::topology::running: Connecting inputs for transform. component=flow_logs
2022-11-17T13:17:16.131230Z DEBUG vector::topology::running: Adding component input to fanout. component=flow_logs fanout_id=in
2022-11-17T13:17:16.131255Z DEBUG vector::topology::running: Connecting inputs for sink. component=my_sink_id
2022-11-17T13:17:16.131277Z DEBUG vector::topology::running: Adding component input to fanout. component=my_sink_id fanout_id=flow_logs
2022-11-17T13:17:16.131305Z DEBUG vector::topology::running: Spawning new source. key=in
2022-11-17T13:17:16.131350Z DEBUG vector::topology::running: Spawning new transform. key=flow_logs
2022-11-17T13:17:16.131381Z TRACE vector::topology::running: Spawning new sink. key=my_sink_id
2022-11-17T13:17:16.131462Z  INFO vector: Vector has started. debug="false" version="0.25.1" arch="x86_64" revision="9125a99 2022-11-07"
2022-11-17T13:17:16.131489Z  INFO vector::app: API is disabled, enable by setting `api.enabled` to `true` and use commands like `vector top`.
2022-11-17T13:17:16.132697Z  INFO vector::topology::builder: Healthcheck: Passed.
2022-11-17T13:17:16.133257Z DEBUG source{component_kind="source" component_id=in component_type=file component_name=in}: vector::topology::builder: Source pump supervisor starting.
2022-11-17T13:17:16.133525Z TRACE vector: Beep.
2022-11-17T13:17:16.133568Z DEBUG source{component_kind="source" component_id=in component_type=file component_name=in}: vector::topology::builder: Source pump starting.
2022-11-17T13:17:16.134526Z DEBUG source{component_kind="source" component_id=in component_type=file component_name=in}: vector::topology::builder: Source starting.
2022-11-17T13:17:16.134565Z  INFO source{component_kind="source" component_id=in component_type=file component_name=in}: vector::sources::file: Starting file server. include=["/var/log/test.log"] exclude=[]
2022-11-17T13:17:16.134805Z DEBUG transform{component_kind="transform" component_id=flow_logs component_type=remap component_name=flow_logs}: vector::topology::builder: Synchronous transform starting.
2022-11-17T13:17:16.135602Z DEBUG sink{component_kind="sink" component_id=my_sink_id component_type=console component_name=my_sink_id}: vector::topology::builder: Sink starting.
2022-11-17T13:17:16.136322Z  INFO source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::checkpointer: Loaded checkpoint data.
2022-11-17T13:17:16.136712Z  INFO source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: vector::internal_events::file::source: Found new file to watch. file=/var/log/test.log
2022-11-17T13:17:16.136778Z DEBUG sink{component_kind="sink" component_id=my_sink_id component_type=console component_name=my_sink_id}: vector::utilization: utilization=0.02086267605633796
2022-11-17T13:17:16.136948Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::file_server: Continue watching file. path="/var/log/test.log"
2022-11-17T13:17:16.136978Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::file_server: Read bytes. path="/var/log/test.log" bytes=146
2022-11-17T13:17:16.136998Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::file_server: Read bytes. path="/var/log/test.log" bytes=151
2022-11-17T13:17:16.137077Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}: vector::internal_events::file::source: Bytes received. byte_size=146 protocol="file" file=/var/log/test.log
2022-11-17T13:17:16.137112Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}: vector::internal_events::file::source: Events received. count=1 byte_size=146 file=/var/log/test.log
2022-11-17T13:17:16.137163Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}: vector::internal_events::file::source: Bytes received. byte_size=151 protocol="file" file=/var/log/test.log
2022-11-17T13:17:16.137184Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}: vector::internal_events::file::source: Events received. count=1 byte_size=151 file=/var/log/test.log
2022-11-17T13:17:16.137228Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-11-17T13:17:16.137248Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}: vector_common::internal_event::events_sent: Events sent. count=2 byte_size=1463 output=_default
2022-11-17T13:17:16.137266Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "flow_logs" })
2022-11-17T13:17:16.137280Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-11-17T13:17:16.137287Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}: vector_core::fanout: Sent item to fanout.
2022-11-17T13:17:16.137307Z TRACE transform{component_kind="transform" component_id=flow_logs component_type=remap component_name=flow_logs}: vector_common::internal_event::events_received: Events received. count=2 byte_size=1463
2022-11-17T13:17:16.137395Z ERROR transform{component_kind="transform" component_id=flow_logs component_type=remap component_name=flow_logs}: vector::internal_events::remap: Mapping failed with event. error="function call error for \"parse_aws_vpc_flow_log\" at (4:204): failed to parse value as i64 (key: `dstport`): `192.168.1.4`" error_type="conversion_failed" stage="processing" internal_log_rate_limit=true
2022-11-17T13:17:16.137432Z ERROR transform{component_kind="transform" component_id=flow_logs component_type=remap component_name=flow_logs}: vector::internal_events::remap: Internal log [Mapping failed with event.] is being rate limited.
2022-11-17T13:17:16.137451Z TRACE transform{component_kind="transform" component_id=flow_logs component_type=remap component_name=flow_logs}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "my_sink_id" })
2022-11-17T13:17:16.137456Z TRACE transform{component_kind="transform" component_id=flow_logs component_type=remap component_name=flow_logs}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-11-17T13:17:16.137460Z TRACE transform{component_kind="transform" component_id=flow_logs component_type=remap component_name=flow_logs}: vector_core::fanout: Sent item to fanout.
2022-11-17T13:17:16.137478Z TRACE transform{component_kind="transform" component_id=flow_logs component_type=remap component_name=flow_logs}: vector_common::internal_event::events_sent: Events sent. count=2 byte_size=1487 output=_default
2022-11-17T13:17:16.137503Z TRACE sink{component_kind="sink" component_id=my_sink_id component_type=console component_name=my_sink_id}: vector_common::internal_event::events_received: Events received. count=2 byte_size=1463
2022-11-17T13:17:16.137813Z TRACE sink{component_kind="sink" component_id=my_sink_id component_type=console component_name=my_sink_id}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=921
2022-11-17T13:17:16.137843Z TRACE sink{component_kind="sink" component_id=my_sink_id component_type=console component_name=my_sink_id}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=279 protocol=console
{"file":"/var/log/test.log","host":"DESKTOP-8LIDEUK","message":"OK use1-az2 - vpc-66546546fdsfsd subnet-45455dfdfdf 166524 166521 egress ACCEPT - - 192.1.2.3 192.168.1.4 22500 11.2.4.1 222 10.0.0.1 8 IPv4 9 411","source_type":"file","timestamp":"2022-11-17T13:17:16.137154400Z"}
2022-11-17T13:17:16.137888Z TRACE sink{component_kind="sink" component_id=my_sink_id component_type=console component_name=my_sink_id}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=926
{"file":"/var/log/test.log","host":"DESKTOP-8LIDEUK","message":"OK use1-az2 - vpc-66546546fdsfsd subnet-45455dfdfdf 166524 166521 egress ACCEPT AMAZON - 192.1.2.3 192.168.1.4 22500 11.2.4.1 222 10.0.0.1 8 IPv4 9 411","source_type":"file","timestamp":"2022-11-17T13:17:16.137204700Z"}
2022-11-17T13:17:16.137906Z TRACE sink{component_kind="sink" component_id=my_sink_id component_type=console component_name=my_sink_id}: vector_common::internal_event::bytes_sent: Bytes sent. byte_size=284 protocol=console
2022-11-17T13:17:17.133568Z TRACE vector: Beep.
2022-11-17T13:17:17.143726Z DEBUG vector::internal_events::file::source: Files checkpointed. count=4 duration_ms=5
2022-11-17T13:17:17.168471Z DEBUG source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::file_server: event_throughput=2.000/sec bytes_throughput=297.000/sec ratios={"discovery": 0.00020829622, "other": 6.4359556e-5, "reading": 6.658888e-5, "sending": 0.0001441305, "sleeping": 0.9995174}
2022-11-17T13:17:17.169871Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::file_server: Continue watching file. path="/var/log/test.log"
2022-11-17T13:17:18.133853Z TRACE vector: Beep.
2022-11-17T13:17:18.144614Z DEBUG vector::internal_events::file::source: Files checkpointed. count=4 duration_ms=0
2022-11-17T13:17:18.195192Z DEBUG source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::file_server: event_throughput=1.000/sec bytes_throughput=148.000/sec ratios={"discovery": 0.0007589226, "other": 0.00013320737, "reading": 3.7163984e-5, "sending": 0.00010784843, "sleeping": 0.9989629}
2022-11-17T13:17:18.195482Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::file_server: Continue watching file. path="/var/log/test.log"
2022-11-17T13:17:19.133770Z TRACE vector: Beep.
2022-11-17T13:17:19.145034Z DEBUG vector::internal_events::file::source: Files checkpointed. count=4 duration_ms=0
2022-11-17T13:17:20.133486Z TRACE vector: Beep.
2022-11-17T13:17:20.146791Z DEBUG vector::internal_events::file::source: Files checkpointed. count=4 duration_ms=0
2022-11-17T13:17:20.244489Z DEBUG source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::file_server: event_throughput=0.000/sec bytes_throughput=74.000/sec ratios={"discovery": 0.00044296854, "other": 8.286793e-5, "reading": 1.9061572e-5, "sending": 5.759857e-5, "sleeping": 0.9993975}
2022-11-17T13:17:20.244717Z TRACE source{component_kind="source" component_id=in component_type=file component_name=in}:file_server: file_source::file_server: Continue watching file. path="/var/log/test.log"
^C2022-11-17T13:17:20.684920Z  INFO vector: Vector has stopped.
2022-11-17T13:17:20.685184Z DEBUG vector::sources::file: Finished sending.
2022-11-17T13:17:20.685227Z DEBUG source{component_kind="source" component_id=in component_type=file component_name=in}: vector::topology::builder: Source pump finished normally.
2022-11-17T13:17:20.685247Z DEBUG source{component_kind="source" component_id=in component_type=file component_name=in}: vector::topology::builder: Source pump supervisor task finished normally.
2022-11-17T13:17:20.685248Z DEBUG source{component_kind="source" component_id=in component_type=file component_name=in}: vector::topology::builder: Source finished normally.
2022-11-17T13:17:20.685288Z DEBUG transform{component_kind="transform" component_id=flow_logs component_type=remap component_name=flow_logs}: vector::topology::builder: Synchronous transform finished normally.
2022-11-17T13:17:20.685328Z DEBUG sink{component_kind="sink" component_id=my_sink_id component_type=console component_name=my_sink_id}: vector::topology::builder: Sink finished normally.
```


### Example Data

OK use1-az2 - vpc-66546546fdsfsd subnet-45455dfdfdf 166524 166521 egress ACCEPT - - 192.1.2.3 192.168.1.4 22500 11.2.4.1 222 10.0.0.1 8 IPv4 9 411
OK use1-az2 - vpc-66546546fdsfsd subnet-45455dfdfdf 166524 166521 egress ACCEPT AMAZON - 192.1.2.3 192.168.1.4 22500 11.2.4.1 222 10.0.0.1 8 IPv4 9 411


### Additional Context

_No response_

### References

_No response_
