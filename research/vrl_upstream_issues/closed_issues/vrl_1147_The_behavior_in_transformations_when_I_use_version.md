# Issue #1147: The behavior in transformations when I use version 0.40.0 of vector with the del(.) function is returning an empty json

- **URL:** https://github.com/vectordotdev/vrl/issues/1147
- **Author:** @madson7
- **Status:** CLOSED (completed)
- **Created:** 2024-11-27T16:24:44Z
- **Closed:** 2024-12-04T15:45:04Z
- **Labels:** vrl:stdlib, meta:awaiting author

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

The behavior in transformations when I use version 0.40.0 of vector with the del(.) function is returning an empty json:

```json
{ }
```
Vector Remap Language (VRL) is an expression-oriented language designed for transforming observability data. This [playground](https://playground.vrl.dev) lets you write a program, run it against an event or events, share it, and see how the events are transformed.
Vector Version:	3d16e345
VRL Version:	0.19.0
```json
{
	"_time": "2024-11-25T12:33:51.177455337Z",
	"timestamp": "2024-11-25T12:33:50.176779920Z"
}
```
```VRL
log = .timestamp 
del(.)
.log_timestamp = log
```
```json
{
	"log_timestamp": "2024-11-25T12:33:50.176779920Z"
}
```
The behavior in transformations when I use version 0.40.0 of vector with the del(.) function is returning an empty json:

```json
{
	"_time": "2024-11-25T12:33:51.177455337Z",
	"timestamp": "2024-11-25T12:33:50.176779920Z"
}
```
```yaml
#vector.yaml
transforms:
  msg_parser:
    type: remap
    inputs:
      - docker
    source: |
      log = .timestamp 
      del(.)
      .log_timestamp = log
```
```bash
$ docker run -ti --rm -v $(pwd):/mnt/ docker.io/timberio/vector:0.40.0-distroless-static validate /mnt/vector.yaml
√ Loaded ["/mnt/vector.yaml"]
√ Component configuration
~ Health check disabled for "http"
----------------------------------
                         Validated
```
Error
```json
{ }
```

### Configuration

```text
api:
  enabled: true
  address: 0.0.0.0:8686

sources:
  docker:
    type: docker_logs

transforms:
  msg_parser:
    type: remap
    inputs:
      - docker
    source: |
      msg_downcase = downcase(string!(.message))
      msg_parse_key_value = parse_key_value!(msg_downcase)
      encode_key_value = encode_key_value(.)
      timestamp_log = to_unix_timestamp(parse_timestamp!(.timestamp, format: "%Y-%m-%dT%H:%M:%S.%fZ"))
      timestamp_parsed = to_unix_timestamp(now())

      namespace = parse_regex!(encode_key_value, r'namespace=(?P<namespace>\w+)', false)
      service_name = parse_regex!(encode_key_value, r'service.name=(?P<service_name>\w+)', false)

      docker = {
        "host": .host,
        "image": .image,
        "container_created_at": .container_created_at,
        "container_name": .container_name
        }
      stack = {
        "namespace": namespace,
        "service_name": service_name
        }

      del(.)

      parse = { 
        "timestamps": {
          "timestamp_log": timestamp_log,
          "timestamp_parsed": timestamp_parsed
        },
        "docker": docker,
        "stack": stack,
        "msg": {
          "msg_downcase": msg_downcase,
          "msg_parse_key_value": msg_parse_key_value
        }
      }

      .log = encode_json(parse)

sinks:
  http:
    type: http
    inputs:
      - msg_parser
    uri: http://9.0.4.206:9428/insert/jsonline?_stream_fields=source_type,host,container_name&_msg_field=log
    encoding:
      codec: json
    framing:
      method: newline_delimited
    compression: gzip
    healthcheck:
      enabled: false
    request:
      headers:
        AccountID: '0'
        ProjectID: '0'
```


### Version

0.40.0

### Debug Output

_No response_

### Example Data
```json
[
  {
    "_time": "2024-11-27T16:21:54.869450219Z",
    "_stream_id": "00000000000000006c25093dad8bf2f8c5fae0fdbc0a1630",
    "_stream": "{container_name=\"semaphore_app.1.rvcq0bpzddvlafu7ixwziz6mg\",host=\"bull\",source_type=\"docker_logs\"}",
    "_msg": "missing _msg field; see https://docs.victoriametrics.com/victorialogs/keyconcepts/#message-field",
    "container_created_at": "2024-11-26T19:00:36.349556757Z",
    "container_id": "0b24d9b15fbe1764149ca7bd7bf22fb3fbe386d1e9cec6e632259a7eca5b1469",
    "container_name": "semaphore_app.1.rvcq0bpzddvlafu7ixwziz6mg",
    "host": "bull",
    "image": "semaphoreui/semaphore:126",
    "label.com.docker.stack.namespace": "semaphore",
    "label.com.docker.swarm.node.id": "9mlqety46qllpelesxvxxgint",
    "label.com.docker.swarm.service.id": "o9el4uqn428dh05a7md9spj9m",
    "label.com.docker.swarm.service.name": "semaphore_app",
    "label.com.docker.swarm.task.id": "rvcq0bpzddvlafu7ixwziz6mg",
    "label.com.docker.swarm.task.name": "semaphore_app.1.rvcq0bpzddvlafu7ixwziz6mg",
    "label.maintainer": "Semaphore UI <support@semui.co>",
    "label.org.opencontainers.image.created": "2024-10-21T11:11:01.004Z",
    "label.org.opencontainers.image.description": "Modern UI and powerful API for Ansible, Terraform, OpenTofu, PowerShell and other DevOps tools.",
    "label.org.opencontainers.image.licenses": "MIT",
    "label.org.opencontainers.image.revision": "f33944e0429f711b24e03600a0c1dab7460b3a2d",
    "label.org.opencontainers.image.source": "https://github.com/semaphoreui/semaphore",
    "label.org.opencontainers.image.title": "semaphore",
    "label.org.opencontainers.image.url": "https://github.com/semaphoreui/semaphore",
    "label.org.opencontainers.image.vendor": "SemaphoreUI",
    "label.org.opencontainers.image.version": "v2.10.32",
    "source_type": "docker_logs",
    "stream": "stdout",
    "timestamp": "2024-11-27T16:21:53.868379720Z"
  }
]
```
### Additional Context

I'm facing a problem when using VRL (Vector Remap Language) in Vector. In the [playground](https://playground.vrl.dev), I can perform all the desired operations, save the results in variables, and then apply del(.) to clean the previous data in the JSON, leaving only what was saved in the variables. Finally, I save the cleaned results in .log, and everything works as expected.

However, when I apply this logic in the transforms block of the vector.yaml file, the behavior is different. When I use del(.), the expected data is not saved in .log, that is, the JSON seems to be completely cleaned and the .log is empty.

If I remove the del(.), I notice that all the operations were performed correctly, but the old data remains in the JSON, without being replaced or overwritten. I also tried an alternative approach, using . = .log without del(.), but I was unsuccessful.

I would like to understand what is causing this difference between the playground and Vector, and what would be the best practice to clean the original JSON and save only the content of the variables processed in .log in vector.yaml.

### References

_No response_
