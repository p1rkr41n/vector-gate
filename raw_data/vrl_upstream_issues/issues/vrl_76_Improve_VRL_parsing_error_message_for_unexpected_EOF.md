# [#76] Improve VRL parsing error message for unexpected EOF

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/76)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2022-03-02T19:40:27Z`
- **Updated At**: `2026-06-01T14:16:38Z`
- **Comments**: 3
- **Labels**: `vrl:diagnostic`, `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/76)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

With config:

```toml
[sources.source0]
type = "stdin"

[transforms.transform0]
type = "filter"
inputs = [ "source0" ]
condition = """ match(string(.name) ?? "", r'(^(machine|apiserver|cluster:capacity|cluster:container|cluster:cpu|cluster:master|cluster:memory|cluster:nodes|cluster:node|container_cpu|container_fs|container_memory|container_network|kube_node|kube_pod_container|kube_pod|node|pod:container_cpu_usage:sum|pod:container_memory_usage_bytes:sum|pod:container)_.*|kube_resourcequota|ALERTS_FOR_STATE|cluster_version)'"""

[sinks.sink0]
inputs = ["transform0"]
type = "console"
encoding.codec = "json"
```

Vector outputs an "unexpected parse error":

```
error[E202]: syntax error
  ┌─ :1:1
  │
1 │  match(string(.name) ?? "", r'(^(machine|apiserver|cluster:capacity|cluster:container|cluster:cpu|cluster:master|cluster:memory|cluster:nodes|cluster:node|container_cpu|container_fs|container_memory|container_network|kube_node|kube_pod_container|kube_pod|node|pod:container_cpu_usage:sum|pod:container_memory_usage_bytes:sum|pod:container)_.*|kube_resourcequota|ALERTS_FOR_STATE|cluster_version)'
  │ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ unexpected error: unexpected parse error
  │
  = see language documentation at https://vrl.dev
```

Due to the lack of a closing `)`.

Seemingly we could do better here with something like `unexpected end-of-input, expected )`.

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

https://discordapp.com/channels/742820443487993987/746070591097798688/948664679083966474

### Version

vector 0.20.0 (x86_64-apple-darwin 2a706a3 2022-02-10)
