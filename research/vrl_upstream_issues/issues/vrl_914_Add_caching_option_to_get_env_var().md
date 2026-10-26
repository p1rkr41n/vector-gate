# [#914] Add caching option to get_env_var()

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/914)
- **Status**: `OPEN`
- **Author**: [@kaarolch](https://github.com/kaarolch)
- **Created At**: `2024-06-27T12:47:39Z`
- **Updated At**: `2026-06-16T13:09:55Z`
- **Comments**: 5
- **Labels**: `vrl:stdlib`, `stdlib:get_env_var`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/914)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

During metric processing, we started using Vector VRL's get_env_var() to pull environment variables and use them as feature flags. Unfortunately, we observed a significant spike in CPU and vector utilization when we used the following configuration:
```
type: "remap"
inputs:
  - metrics_ingestion
source: |
  cardinality_limit, err = get_env_var("CARDINALITY_LIMIT")
      if err == null {
        .tags.cardinality_limit = cardinality_limit
      } else {
        .tags.cardinality_limit = "false"
      }
  metrics_processor, err = get_env_var("METRICS_PROCESSOR")
      if err == null {
        .tags.metrics_processor = metrics_processor
      } else {
        .tags.metrics_processor = "false"
      }
  tags_filter, err = get_env_var("TAGS_FILTER")
      if err == null {
        .tags.tags_filter = tags_filter
      } else {
        .tags.tags_filter = "false"
      }
```
This was applied to every metric. Now, we have decided to add this transformation only to the metrics that really need it (around 30% of all processed metrics), and we were able to save about 2-3 Kubernetes vCPUs (a drop from ~10 vCPUs to 7-8 vCPUs). Transform change was deployed around 13:15.
![image](https://github.com/vectordotdev/vector/assets/16565131/04d69e9d-7aae-40cf-98cb-1519ed445b1d)

The problem started increasing when we added more than two environment variable checks.

### Attempted Solutions

As I mentioned, we are currently trying to minimize the use of environment variable checks. Now, we are also experimenting with [data enrichment](https://vector.dev/guides/level-up/csv-enrichment-guide/). During container startup, we will render an enrichment table and add the data as extra tags during metric remapping.

### Proposal

Is there any chance to support environment variable caching with a TTL? When using remap to check for very static environment variables like ENV and VERSION, which do not change during runtime, we could set a TTL to avoid querying the system each time we set the same variable. [Reference](https://github.com/vectordotdev/vector/blob/476016b28890df879789c5408dfab5c4eb80c33e/build.rs#L16).

### References

_No response_

### Version

0.37.0
