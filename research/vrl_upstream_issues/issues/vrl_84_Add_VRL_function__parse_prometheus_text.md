# [#84] Add VRL function: parse_prometheus_text

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/84)
- **Status**: `OPEN`
- **Author**: [@roganartu](https://github.com/roganartu)
- **Created At**: `2022-01-13T23:20:40Z`
- **Updated At**: `2026-06-01T14:16:29Z`
- **Comments**: 4
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/84)

---

## Description

### Community Note

* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment

### Current Vector Version

```
vector 0.19.0 (x86_64-unknown-linux-gnu da60b55 2021-12-28)
```

### Use-cases

A common way to create small, custom prometheus exporters is to write scripts that emit Prometheus textfile format files to a directory that is then read by [node_exporter](https://github.com/prometheus/node_exporter). This requires managing scheduling (via cron or systemd timer), and doesn't provide many metrics about the process itself (eg runtime, exit code, etc).

A nice alternative to this would be a vector pipeline of `sources.exec -> transforms.remap -> sinks.prometheus`, but the exec emits a `log` and parsing that into `metrics` for the prometheus sink to consume would require lua and would likely be error prone and slow.

### Attempted Solutions

I considered trying to write a lua PoC, but decided against it because it seems like a bad idea. I looked through the VRL docs and saw a number of `parse_` functions for various different formats, but none for Prometheus data. I also searched github issues for existing "prometheus" issues but saw nothing obviously duplicate of this. I apologise if I missed something obvious.

### Proposal

Add a VRL function: `parse_prometheus_text`.

It should accept a Prometheus textfile format string, and return a vector metrics object. Example usage:
```
[sources.my_exec]
type = "exec"
mode = "scheduled"
scheduled.exec_interval_secs = 10
command = ["my_prometheus_command"]

[transforms.parse_prometheus_output]
type = "remap"
inputs = [ "my_exec" ]
source = '''
. = parse_prometheus_text!(.message)
'''

[sinks.prometheus]
type = "prometheus_exporter"
inputs = [ "parse_prometheus_output" ]
address = "0.0.0.0:9598"
default_namespace = "vector"
```

The metrics printed to stdout by `my_prometheus_command` should be exposed via `0.0.0.0:9598/metrics` like any other input to that sink would be.

The other prometheus features (specifically the prometheus exporter source) suggest that vector is already capable of robustly parsing Prometheus text format.
