# [#686] `datadog_search` syntax filters doesn't work when key contains `.`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/686)
- **Status**: `OPEN`
- **Author**: [@smitthakkar96](https://github.com/smitthakkar96)
- **Created At**: `2023-03-27T13:24:28Z`
- **Updated At**: `2026-06-01T14:06:33Z`
- **Comments**: 5
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/686)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

When using datadog_search syntax in the filter or route transform, if the attribute key has `.` in it, the search doesn't work. See the example test cases in the configuration. 

### Configuration

``` toml
[sources.vector_primary]
type = "vector"
address = "0.0.0.0:8080"

[transforms.parse_json]
inputs = ["vector_primary"]
type = "remap"
source = """
.custom = parse_json(.custom) ?? {}
"""

[transforms.filter_health_check_logs]
inputs = ["parse_json"]
type = "filter"
condition = { type = "datadog_search", source = "@grpc.method:HealthCheck" }

[transforms.filter_channel]
inputs = ["parse_json"]
type = "filter"
condition = { type = "datadog_search", source = "@channel:api" }

# This is working

[[tests]]
  name = "test_filter_health_check_logs"
  [[tests.inputs]]
    type = "log"
    insert_at = "parse_json"
    [tests.inputs.log_fields]
      custom = '{"grpc.method": "HealthCheck", "squad": "testing-squad"}'
      message = 'foo bar'

  [[tests.outputs]]
    extract_from = "filter_health_check_logs"
    [[tests.outputs.conditions]]
      type = "vrl"
      source = """
        log(.)
        assert_eq!(.message, "foo bar")
      """

# This is not working

[[tests]]
  name = "test_filter_channel"
  [[tests.inputs]]
    type = "log"
    insert_at = "parse_json"
    [tests.inputs.log_fields]
      custom = '{"grpc.method": "HealthCheck", "channel": "api"}'
      message = 'foo bar'

  [[tests.outputs]]
    extract_from = "filter_channel"
    [[tests.outputs.conditions]]
      type = "vrl"
      source = """
        log(.)
        assert_eq!(.message, "foo bar")
      """
```


### Version

`vector 0.27.0`

### Debug Output

_No response_

### Example Data

See the test case

### Additional Context

We are in the process of adopting Vector in our organisation, our goal is to migrate exclusion filters from Datadog Log Index to Vector, and we have many indexes. Using `datadog_search` syntax would make migration easy for us, otherwise, we will have to translate 500+ filters to VRL. This is blocking us from adopting Vector for log exclusion and sampling. 

### References

_No response_
