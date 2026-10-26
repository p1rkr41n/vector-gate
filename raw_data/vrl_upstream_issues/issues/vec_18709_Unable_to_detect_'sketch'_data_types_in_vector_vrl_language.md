# [#18709] Unable to detect 'sketch' data types in vector vrl language

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/18709)
- **Status**: `OPEN`
- **Author**: [@seanlowcy77](https://github.com/seanlowcy77)
- **Created At**: `2023-09-28T18:25:05Z`
- **Updated At**: `2026-05-29T23:17:25Z`
- **Comments**: 2
- **Labels**: `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/18709)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Hi Vector team,

I currently have distribution metrics coming from a DD agent metrics source. I wanted to route these metrics within vector. However I noticed they have tags like
"sketch": {
    "sketch": {
      "AgentDDSketch": {

When I try to route them via vrl with a condition like '.type != sketch' it doesnt work. This seems to be a bug as mentioned by @jszwedko.

This was also previously discussed in https://discord.com/channels/742820443487993987/1156386370160443462/1156386370160443462

### Configuration

```text
Config:

[transforms.route_post_aggr_metrics]
type = "route"
inputs = ["aggregate_metrics"]
route.to_add_vector_hostname = '.type != "sketch"'
```

Unit test:
```
[[tests.inputs]]
insert_at = "route_post_aggr_metrics"
type = "metric"

[tests.inputs.metric]
kind = "incremental"
namespace = "XXX"
name = "YYY"
sketch = { sketch = { AgentDDSketch = {bins = {k = [1], n = [1]}, count = 1,min = 1, max = 1, sum = 1, avg = 1}}}


[[tests.outputs]]
extract_from = "route_post_aggr_metrics._unmatched"

[[tests.outputs.conditions]]
type = "vrl"
source = """
assert_eq!(.namespace, "XXX")
assert_eq!(.name, "YYY")
```
```


### Version

vector 0.32.2

### Debug Output

```text
checks for transforms ["route_post_aggr_metrics._unmatched"] failed: no events 
received. Topology may be disconnected or transform is missing inputs.
I guess implying that no events are going through ._unmatched (indicating that its going through to_add_vector_hostname)
```


### Example Data

_No response_

### Additional Context

_No response_

### References

https://discord.com/channels/742820443487993987/1156386370160443462/1156386370160443462
