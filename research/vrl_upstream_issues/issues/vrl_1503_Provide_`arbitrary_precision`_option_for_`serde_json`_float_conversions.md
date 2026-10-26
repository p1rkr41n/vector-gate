# [#1503] Provide `arbitrary_precision` option for `serde_json` float conversions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1503)
- **Status**: `OPEN`
- **Author**: [@DominikMoelter](https://github.com/DominikMoelter)
- **Created At**: `2025-08-27T14:34:22Z`
- **Updated At**: `2026-03-16T11:57:02Z`
- **Comments**: 5
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1503)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

When using [parse_json()](https://vector.dev/docs/reference/vrl/functions/#parse_json) with some float numbers the return value contains numbers which do not match with the input data.

I'm using this config
```yaml
sources:
  dummy_logs:
    type: "demo_logs"
    format: "shuffle"
    interval: 5
    lines:
    - '{"coordinates":[0.12379999458789825,0.05209999904036522,-0.1266999989748001]}'
    - '{"coordinates":[-0.24199999868869781,-0.07459999620914459,-0.0032999999821186066]}'
      
transforms:
  parse_json:
    type: remap
    inputs: 
      - dummy_logs
    source: |
      . = parse_json!(.message)

sinks:
  console_out:
    type: console
    inputs:
      - parse_json
    encoding:
      codec: json
```

The output shows

```bash
2025-08-27T14:29:19.211496Z  INFO vector::app: Log level is enabled. level="info"
2025-08-27T14:29:19.212886Z  INFO vector::app: Loading configs. paths=["."]
2025-08-27T14:29:19.216547Z  INFO vector::topology::running: Running healthchecks.
2025-08-27T14:29:19.216665Z  INFO vector: Vector has started. debug="false" version="0.49.0" arch="x86_64" revision="dc7e792 2025-08-12 13:47:08.632326804"
2025-08-27T14:29:19.216682Z  INFO vector::app: API is disabled, enable by setting `api.enabled` to `true` and use commands like `vector top`.
2025-08-27T14:29:19.216810Z  INFO vector::topology::builder: Healthcheck passed.
{"coordinates":[-0.2419999986886978,-0.07459999620914459,-0.0032999999821186066]}
{"coordinates":[0.12379999458789824,0.05209999904036522,-0.1266999989748001]}
```

As you can see in this example both first array entries do not match with the input data. This does not always happen, so there is also data which is parsed correctly.



### Configuration

```text

```

### Version

vector 0.49.0 (x86_64-unknown-linux-gnu dc7e792 2025-08-12 13:47:08.632326804)

### Debug Output

```text

```

### Example Data

```json
{"coordinates":[0.12379999458789825,0.05209999904036522,-0.1266999989748001]}
{"coordinates":[-0.24199999868869781,-0.07459999620914459,-0.0032999999821186066]}
```

### Additional Context

_No response_

### References

_No response_
