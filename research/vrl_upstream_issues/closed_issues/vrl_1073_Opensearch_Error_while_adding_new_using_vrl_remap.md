# Issue #1073: Opensearch Error while adding new using vrl remap

- **URL:** https://github.com/vectordotdev/vrl/issues/1073
- **Author:** @7czl
- **Status:** CLOSED (completed)
- **Created:** 2024-10-15T09:02:01Z
- **Closed:** 2024-10-15T15:52:40Z
- **Labels:** None

## Description

[sources.kafka]
  type = "kafka"
  bootstrap_servers = "kfk-tmonix01:9092,kfk-tmonix01sg-02:9092,kfk-tmonix01sg-03:9092"
  group_id = "vector-consumer-group"
  topics = ["pods-kafka"]
  session_timeout_ms = 10_000
  socket_timeout_ms = 60_000
  commit_interval_ms = 5_000
  drain_timeout_ms = 2_500
  fetch_wait_max_ms = 100

[transforms.pods]
  type = "remap"
  inputs = ["kafka"]
  drop_on_abort = true
  drop_on_error = true
  reroute_dropped = true
  metric_tag_values = "single"
  source = '''
        msg = parse_json!(string!(.message))
        log(msg.message)
        .a = msg.file # just add .a the error prompts out.
  '''
[sinks.opensearch]
  type = "elasticsearch"
  inputs = [ "pods" ]
  api_version = "v8"
  endpoints = [ "https://localhost:9200" ]
  bulk.index = "vector-%Y-%m-%d"
  auth.strategy = "basic"
  auth.user = "vector-user"
  auth.password = "password"
  tls.verify_certificate = false

2024-10-15T08:45:33.228227Z  WARN sink{component_kind="sink" component_id=opensearch component_type=elasticsearch}: vector_core::
2024-10-15T08:45:33.244673Z  INFO vector::topology::running: Running healthchecks.
2024-10-15T08:45:33.244823Z  INFO vector: Vector has started. debug="false" version="0.41.1" arch="x86_64" revision="745babd 2024
2024-10-15T08:45:33.246806Z  INFO vector::internal_events::api: API server running. address=127.0.0.1:8686 playground=http://127.
2024-10-15T08:45:33.251662Z  INFO vector::topology::builder: Healthcheck passed.
2024-10-15T08:45:33.263141Z  INFO transform{component_kind="transform" component_id=extract_file component_type=remap}: vrl::stdl
2024-10-15T08:45:33.263263Z  INFO transform{component_kind="transform" component_id=extract_file component_type=remap}: vrl::stdl
2024-10-15T08:45:34.274251Z  INFO transform{component_kind="transform" component_id=extract_file component_type=remap}: vrl::stdl
2024-10-15T08:45:34.274424Z  INFO transform{component_kind="transform" component_id=extract_file component_type=remap}: vrl::stdl
2024-10-15T08:45:34.536375Z  INFO transform{component_kind="transform" component_id=extract_file component_type=remap}: vrl::stdl
2024-10-15T08:45:35.011258Z ERROR sink{component_kind="sink" component_id=opensearch component_type=elasticsearch}:request{reques
2024-10-15T08:45:35.013257Z ERROR sink{component_kind="sink" component_id=opensearch component_type=elasticsearch}:request{reques
2024-10-15T08:45:35.013285Z ERROR sink{component_kind="sink" component_id=opensearch component_type=elasticsearch}:request{reques
2024-10-15T08:45:35.013318Z ERROR sink{component_kind="sink" component_id=opensearch component_type=elasticsearch}:request{reques
2024-10-15T08:45:35.294785Z ERROR sink{component_kind="sink" component_id=opensearch component_type=elasticsearch}:request{requesd\":\"4zBaj5IBHlWLVcZSpPOr\",\"status\":400,\"error\":{\"type\":\"illegal_argument_exception\",\"reason\":\"Limit of total fields [1000] has been exceeded\"}}},{\"index\":{\"_index\":\"vector-2024-10-15\",\"_id\":\"5DBaj5IBHlWLVcZSpPOr\",\"status\":400,\"error\":{\"type\":\"illegal_argument_exception\",\"reason\":\"Limit of total fields [1000] has been exceeded\"}}},{\"index\":{\"_index\":\"vector-2024-10-15\",\"_id\":\"5TBaj5IBHlWLVcZSpPOr\",\"status\":400,\"error\":{\"type\":\"illegal_argument_exception\",\"reason\":\"Limit of total fields [1000] has been exceeded\"}}},{\"index\":{\"_index\":\"vector-2024-10-15\",\"_id\":\"5jBaj5IBHlWLVcZSpPOr\",\"status\":400,\"error\":{\"type\":\"illegal_argument_exception\",\"reason\":\"Limit of total fields [1000] has been exceeded\"}}}]}" }
