# [#1396] VRL error message advice on wrong line

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1396)
- **Status**: `OPEN`
- **Author**: [@alexandrebrg](https://github.com/alexandrebrg)
- **Created At**: `2023-12-12T22:47:39Z`
- **Updated At**: `2026-06-01T14:07:24Z`
- **Comments**: 3
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1396)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Hello! 👋 

I am currently giving a try to vector, and I started to use VRL to remap my data. I'm using a `file` source which read files that are json (one json object per line). I transform it to match the format I want (it's not prometheus format if you wonder, but Warp10 format).

The problem is  in my second transform (`warp10`), the VRL compiler fails saying that the line `.data = set!(.data, [new_key], value)` is faillible while it's not. In fact, it's the line just above it that is fallible and that should be advised to make infallible.

Logs:

```
/tmp/vector
❯ vector --config config.yaml
2023-12-12T22:42:12.031631Z  INFO vector::app: Log level is enabled. level="vector=info,codec=info,vrl=info,file_source=info,tower_limit=info,rdkafka=info,buffers=info,lapin=info,kube=info"
2023-12-12T22:42:12.032442Z  INFO vector::app: Loading configs. paths=["config.yaml"]
2023-12-12T22:42:12.044065Z ERROR vector::topology::builder: Configuration error. error=Transform "warp10":
error[E103]: unhandled fallible assignment
  ┌─ :8:11
  │
8 │   .data = set!(.data, [new_key], value)
  │   ------- ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  │   │       │
  │   │       this expression is fallible
  │   │       update the expression to be infallible
  │   │       note if an argument type is invalid it can render a function fallible
  │   or change this to an infallible assignment:
  │   .data, err = set(.data, [new_key], value)
  │
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = see functions characteristics documentation at https://vrl.dev/expressions/#function-call-characteristics
  = learn more about error code 103 at https://errors.vrl.dev/103
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
``` 


### Configuration

```yaml
sources:
  fdb_logs:
    ignore_checkpoints: true
    type: "file"
    data_dir: "/tmp/vector/"
    include:
      - "/tmp/vector/**/*.log"

transforms:
  process_metrics:
    type: remap
    inputs:
      - fdb_logs
    source: |
      . = parse_json!(.message)

      structured = {}
      structured.Type = .Type
      structured.data = .

      del(structured.data.Type)

      metrics = {}
      for_each(object!(structured.data)) -> |key, value| {
        metric_name = "foundationdb." + downcase(key)
        metrics, err = set(metrics, [metric_name], value)
        if err != null {
          log("Unable to parse " + err, level: "error")
        }
      }

      structured.data = metrics
      . = structured

  warp10:
    type: remap
    inputs:
      - process_metrics
    source: |
      event_type = .Type
      for_each(object!(.data)) -> |key, value| {
        log_time = format_timestamp!(now(),"%s")
        labels, err = "{host=" + get_hostname!() + ",type=" + downcase(event_type) + "}"
        new_key = key + labels
        # BUG IS HERE: remove is fallible, but compiler advice to fix `set!()`
        remove(.data, [key])
        .data = set!(.data, [new_key], value)
      }
sinks:
  out:
    inputs:
      - warp10
    type: "console"
    encoding:
      codec: "json"
```


### Version

vector 0.34.0 (x86_64-apple-darwin c909b66 2023-11-07 15:07:26.748571656)

### Debug Output

```text
2023-12-12T22:47:05.722017Z DEBUG vector::app: Internal log rate limit configured. internal_log_rate_secs=10
2023-12-12T22:47:05.722295Z  INFO vector::app: Log level is enabled. level="vector=trace,codec=trace,vrl=trace,file_source=trace,tower_limit=trace,rdkafka=trace,buffers=trace,lapin=trace,kube=trace"
2023-12-12T22:47:05.722309Z DEBUG vector::app: messaged="Building runtime." worker_threads=10
2023-12-12T22:47:05.723365Z  INFO vector::app: Loading configs. paths=["config.yaml"]
2023-12-12T22:47:05.725579Z DEBUG vector::config::loading: No secret placeholder found, skipping secret resolution.
2023-12-12T22:47:05.731554Z DEBUG vector::topology::builder: Building new source. component=fdb_logs
2023-12-12T22:47:05.731980Z DEBUG vector::topology::builder: Building new transform. component=process_metrics
2023-12-12T22:47:05.733744Z DEBUG vector::topology::builder: Building new transform. component=warp10
2023-12-12T22:47:05.735160Z DEBUG vector::topology::builder: Building new sink. component=out
2023-12-12T22:47:05.736101Z ERROR vector::topology::builder: Configuration error. error=Transform "warp10":
error[E103]: unhandled fallible assignment
  ┌─ :8:11
  │
8 │   .data = set!(.data, [new_key], value)
  │   ------- ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
  │   │       │
  │   │       this expression is fallible
  │   │       update the expression to be infallible
  │   │       note if an argument type is invalid it can render a function fallible
  │   or change this to an infallible assignment:
  │   .data, err = set(.data, [new_key], value)
  │
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = see functions characteristics documentation at https://vrl.dev/expressions/#function-call-characteristics
  = learn more about error code 103 at https://errors.vrl.dev/103
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```
```


### Example Data

```
{"Type":"ProcessMetrics","ID":"0000000000000000","Elapsed":"5.00096","CPUSeconds":"2.97023","DiskIdleSeconds":"1.17996","DiskReadSeconds":"5.00096","DiskWriteSeconds":"5.00096"}
```

### Additional Context

_No response_

### References

_No response_
