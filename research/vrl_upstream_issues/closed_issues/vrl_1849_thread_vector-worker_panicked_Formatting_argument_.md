# Issue #1849: thread 'vector-worker' panicked: Formatting argument out of range

- **URL:** https://github.com/vectordotdev/vrl/issues/1849
- **Author:** @charlie0129
- **Status:** CLOSED (completed)
- **Created:** 2025-08-18T11:07:09Z
- **Closed:** 2026-07-07T19:47:19Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Vector randomly panics with the following logs (see debug output).


### Configuration

```text
data_dir: /vector-data-dir
api:
  enabled: false
  address: 0.0.0.0:8686
  playground: true
sources:
  k8s:
    type: kubernetes_logs
    node_annotation_fields:
      node_labels: ""
    max_line_bytes: 2097152 # 2MiB
  internal_metrics:
    type: internal_metrics
transforms:
  parse_k8s_logs:
    type: remap
    inputs: [k8s]
    source: |
      .log = parse_json(.message) ??
          parse_key_value(.message, key_value_delimiter: "=", field_delimiter: " ", whitespace: "strict", accept_standalone_key: false) ??
          null
      .cluster = "xxx"
      .vendor  = "xxx"
      .region  = "xxx"
      .mtype   = "cpu"
  filter_k8s_logs: # kubernetes_logs collects all logs, we filter out old logs to save resources
    type: filter
    inputs: [parse_k8s_logs]
    condition: 'to_unix_timestamp(timestamp!(.timestamp)) > to_unix_timestamp(now()) - 2 * 60' # Only fetch logs from the last 2 minutes
sinks:
  exporter:
    type: prometheus_exporter
    address: 0.0.0.0:9090
    inputs: [internal_metrics]
  vlogs:
    type: elasticsearch
    inputs: [filter_k8s_logs]
    auth:
      strategy: basic
      user: xxx
      password: xxx
    endpoints: ["https://xxx/insert/elasticsearch"]
    mode: bulk
    api_version: v8
    compression: zstd
    batch: # batch size is increased to improve compression ratio
      max_bytes: 67108864 # 64MiB
      max_events: 99999999 # do not limit events, only bytes
      timeout_secs: 120 # 2 minutes
    buffer:
      type: disk
      max_size: 536870912 # 512MiB
      # max_events: 1000000 # do not limit events, only size
    distribution:
      retry_initial_backoff_secs: 5
    healthcheck:
      enabled: false
    request:
      headers:
        VL-Time-Field: timestamp
        VL-Stream-Fields: stream,kubernetes.pod_name,kubernetes.container_name,kubernetes.pod_namespace
        VL-Msg-Field: message,_message,msg,_msg,log.msg,log.message,log
        AccountID: "0"
        ProjectID: "0"
```

### Version

0.49.0

### Debug Output

```text
vector thread 'vector-worker' panicked at /cargo/registry/src/index.crates.io-1949cf8c6b5b557f/nom-language-0.1.0/src/error.rs:210:37:
vector Formatting argument out of range
vector stack backtrace:
vector    0:     0x7fd565a16f76 - <std::sys::backtrace::BacktraceLock::print::DisplayBacktrace as core::fmt::Display>::fmt::h755bd739a9a8330b
vector    1:     0x7fd564ca0e33 - core::fmt::write::ha6dc9f3e0fc90354
vector    2:     0x7fd565a1693f - std::io::Write::write_fmt::ha6203d3ee181dafd
vector    3:     0x7fd565a16d53 - std::sys::backtrace::BacktraceLock::print::hfba0c32ab558acd9
vector    4:     0x7fd565a1651a - std::panicking::rust_panic_with_hook::hcbca57a4f53780db
vector    5:     0x7fd565a5b9e5 - std::panicking::begin_panic_handler::{{closure}}::h6aad19e1296c91fb
vector    6:     0x7fd565a5b979 - std::sys::backtrace::__rust_end_short_backtrace::he6330e86917e67b5
vector    7:     0x7fd565a6124c - __rustc[4794b31dd7191200]::rust_begin_unwind
vector    8:     0x7fd56423beff - core::panicking::panic_fmt::h742c54b11a074f59
vector    9:     0x7fd568eb6ac6 - nom_language::error::convert_error::he3ab67a1b7e4aeea
vector   10:     0x7fd568ef16e2 - <vrl::compiler::expression::function::FunctionExpressionAdapter<T> as vrl::compiler::expression::Expression>::resolve::h5e8ce1a9e3c782c5
vector   11:     0x7fd568d4b157 - <vrl::compiler::expression::function_call::FunctionCall as vrl::compiler::expression::Expression>::resolve::hf240456b180ef0d3
vector   12:     0x7fd568d47367 - <vrl::compiler::expression::Expr as vrl::compiler::expression::Expression>::resolve::haf5bac83802dee05
vector   13:     0x7fd568d49e1c - <vrl::compiler::expression::op::Op as vrl::compiler::expression::Expression>::resolve::h9fa6378653a329fd
vector   14:     0x7fd568d473c2 - <vrl::compiler::expression::Expr as vrl::compiler::expression::Expression>::resolve::haf5bac83802dee05
vector   15:     0x7fd568d499f2 - <vrl::compiler::expression::op::Op as vrl::compiler::expression::Expression>::resolve::h9fa6378653a329fd
vector   16:     0x7fd568d473c2 - <vrl::compiler::expression::Expr as vrl::compiler::expression::Expression>::resolve::haf5bac83802dee05
vector   17:     0x7fd568d4755c - <vrl::compiler::expression::Expr as vrl::compiler::expression::Expression>::resolve::haf5bac83802dee05
vector   18:     0x7fd568d64d23 - vrl::compiler::runtime::Runtime::resolve::h62ab96db4818e672
vector   19:     0x7fd567f41206 - <vector::transforms::remap::Remap<Runner> as vector_core::transform::SyncTransform>::transform::h5ad9867476952795
vector   20:     0x7fd567f43fb7 - vector_core::transform::SyncTransform::transform_all::h89f994b585063f2d
vector   21:     0x7fd56883017f - <tracing::instrument::Instrumented<T> as core::future::future::Future>::poll::h43d72c15bc7d20ac
vector   22:     0x7fd5688305a0 - tokio::runtime::task::raw::poll::h0f8f299a7709ec73
vector   23:     0x7fd565aca8ef - tokio::runtime::scheduler::multi_thread::worker::Context::run_task::h1bbd3ed6414b4f30
vector   24:     0x7fd565ac8943 - tokio::runtime::scheduler::multi_thread::worker::run::h482fc547e605cbba
vector   25:     0x7fd565ad2189 - tokio::runtime::task::raw::poll::he4e728f05bd411ae
vector   26:     0x7fd565aa408b - std::sys::backtrace::__rust_begin_short_backtrace::hf4fc553021301660
vector   27:     0x7fd565aac294 - core::ops::function::FnOnce::call_once{{vtable.shim}}::hc9d9af022b7da2da
vector   28:     0x7fd565a6173b - std::sys::pal::unix::thread::Thread::new::thread_start::hd5ffee2aac5a17bf
vector
vector thread 'vector-worker' panicked at src/topology/builder.rs:1008:30:
vector internal error: entered unreachable code: join error or bad poll
vector stack backtrace:
vector    0:     0x7fd565a16f76 - <std::sys::backtrace::BacktraceLock::print::DisplayBacktrace as core::fmt::Display>::fmt::h755bd739a9a8330b
vector    1:     0x7fd564ca0e33 - core::fmt::write::ha6dc9f3e0fc90354
vector    2:     0x7fd565a1693f - std::io::Write::write_fmt::ha6203d3ee181dafd
vector    3:     0x7fd565a16d53 - std::sys::backtrace::BacktraceLock::print::hfba0c32ab558acd9
vector    4:     0x7fd565a1651a - std::panicking::rust_panic_with_hook::hcbca57a4f53780db
vector    5:     0x7fd565a5b9e5 - std::panicking::begin_panic_handler::{{closure}}::h6aad19e1296c91fb
vector    6:     0x7fd565a5b979 - std::sys::backtrace::__rust_end_short_backtrace::he6330e86917e67b5
vector    7:     0x7fd565a6124c - __rustc[4794b31dd7191200]::rust_begin_unwind
vector    8:     0x7fd56423beff - core::panicking::panic_fmt::h742c54b11a074f59
vector    9:     0x7fd56882d884 - vector::topology::builder::Runner::run_concurrently::{{closure}}::he4474e10ef3f6edc
vector   10:     0x7fd568825bc5 - vector::topology::builder::build_sync_transform::{{closure}}::h47ba1de404356d99
vector   11:     0x7fd568799a62 - <tracing::instrument::Instrumented<T> as core::future::future::Future>::poll::h9eed0458fea094eb
vector   12:     0x7fd56879a7ee - tokio::runtime::task::raw::poll::ha150d43850a62f73
vector   13:     0x7fd565aca8b1 - tokio::runtime::scheduler::multi_thread::worker::Context::run_task::h1bbd3ed6414b4f30
vector   14:     0x7fd565ac8943 - tokio::runtime::scheduler::multi_thread::worker::run::h482fc547e605cbba
vector   15:     0x7fd565ad2189 - tokio::runtime::task::raw::poll::he4e728f05bd411ae
vector   16:     0x7fd565aa408b - std::sys::backtrace::__rust_begin_short_backtrace::hf4fc553021301660
vector   17:     0x7fd565aac294 - core::ops::function::FnOnce::call_once{{vtable.shim}}::hc9d9af022b7da2da
vector   18:     0x7fd565a6173b - std::sys::pal::unix::thread::Thread::new::thread_start::hd5ffee2aac5a17bf
vector 2025-08-18T11:02:04.465897Z ERROR transform{component_kind="transform" component_id=parse_k8s_logs component_type=remap}: vector::topology: An error occurred that Vector couldn't handle: the task panicked and was aborted.
vector 2025-08-18T11:02:04.465949Z  INFO vector: Vector has stopped.
vector 2025-08-18T11:02:04.468152Z  INFO vector::topology::running: Shutting down... Waiting on running components. remaining_components="exporter, filter_k8s_logs, k8s, internal_metrics, vlogs, parse_k8s_logs" time_remaining="59 seconds left"
```

### Example Data

_No response_

### Additional Context

This is Vector running in Kubernetes (using official helm chart)

Values

```yaml
role: "Agent"
updateStrategy:
  type: RollingUpdate
  rollingUpdate:
    maxUnavailable: 20%
tolerations:
  - key: node-role.kubernetes.io/master
    operator: Exists
    effect: NoSchedule
  - key: node-role.kubernetes.io/control-plane
    operator: Exists
    effect: NoSchedule
args:
  - -w
  - --config-dir
  - /etc/vector/
containerPorts:
  - name: prom-exporter
    containerPort: 9090
    protocol: TCP
service:
  enabled: false
useMyConfig: true
resources:
  requests:
    memory: "512Mi"
    cpu: "100m"
  limits:
    memory: "4Gi"
    cpu: "8000m"
initContainers:
  - name: set-inotify
    image: alpine:3.22
    imagePullPolicy: IfNotPresent
    command:
      - sh
      - -c
      - sysctl -w fs.inotify.max_user_instances=4096
    securityContext:
      privileged: true
env:
  - name: RUST_BACKTRACE
    value: full
podMonitor:
  enabled: true
  additionalLabels:
    release: kube-prometheus-stack
podPriorityClassName: system-cluster-critical # slightly lower than system-node-critical

```

### References

_No response_
