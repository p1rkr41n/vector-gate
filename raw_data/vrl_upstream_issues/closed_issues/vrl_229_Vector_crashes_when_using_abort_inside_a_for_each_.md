# Issue #229: Vector crashes when using `abort` inside a `for_each` function

- **URL:** https://github.com/vectordotdev/vrl/issues/229
- **Author:** @marcojck
- **Status:** CLOSED (completed)
- **Created:** 2022-06-29T13:49:59Z
- **Closed:** 2026-05-01T18:24:56Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Vector crashes when using `abort` inside a `for_each` function.

### Configuration

```text
sources:
  logs:
    type: demo_logs
    format: shuffle
    lines:
      - line 2 abort

transforms:
    remap:
      type: remap
      inputs: [logs]
      drop_on_error: true
      drop_on_abort: true
      reroute_dropped: true
      source: |-
        for_each(split!(.message, " ")) -> |i, v| {
          log("Processing value '" + string!(v) + "'", "info", 0)
          if (v == "abort") {
            abort
          }
        }

sinks:
  remap_console_sink:
    type: console
    inputs: [remap]
    target: stdout
    encoding: json

  remap_console_dropped_sink:
    type: console
    inputs: [remap.dropped]
    target: stdout
    encoding: json
```


### Version

vector 0.22.2 (x86_64-unknown-linux-gnu 0024c92 2022-06-15)

### Debug Output

```text
2022-06-29T13:45:32.956113Z  INFO vector::app: Log level is enabled. level="vector=trace,codec=trace,vrl=trace,file_source=trace,tower_limit=trace,rdkafka=trace,buffers=trace,kube=trace"
2022-06-29T13:45:32.956199Z  INFO vector::app: Loading configs. paths=["config.yaml"]
2022-06-29T13:45:32.958444Z DEBUG vector::topology::builder: Building new source. component=logs
2022-06-29T13:45:32.958748Z DEBUG vector::topology::builder: Building new transform. component=remap
2022-06-29T13:45:32.959344Z DEBUG vector::topology::builder: Building new sink component=remap_console_dropped_sink
2022-06-29T13:45:32.959422Z DEBUG vector::topology::builder: Building new sink component=remap_console_sink
2022-06-29T13:45:32.959523Z  INFO vector::topology::running: Running healthchecks.
2022-06-29T13:45:32.959546Z DEBUG vector::topology::running: Connecting changed/added component(s).
2022-06-29T13:45:32.959578Z DEBUG vector::topology::running: Configuring outputs for source. component=logs
2022-06-29T13:45:32.959604Z DEBUG vector::topology::running: Configuring output for component. component=logs output_id=None
2022-06-29T13:45:32.959619Z DEBUG vector::topology::running: Configuring outputs for transform. component=remap
2022-06-29T13:45:32.959630Z DEBUG vector::topology::running: Configuring output for component. component=remap output_id=Some("dropped")
2022-06-29T13:45:32.959642Z DEBUG vector::topology::running: Configuring output for component. component=remap output_id=None
2022-06-29T13:45:32.959653Z DEBUG vector::topology::running: Connecting inputs for transform. component=remap
2022-06-29T13:45:32.959673Z DEBUG vector::topology::running: Adding component input to fanout. component=remap fanout_id=logs
2022-06-29T13:45:32.959693Z DEBUG vector::topology::running: Connecting inputs for sink. component=remap_console_dropped_sink
2022-06-29T13:45:32.959718Z DEBUG vector::topology::running: Adding component input to fanout. component=remap_console_dropped_sink fanout_id=remap.dropped
2022-06-29T13:45:32.959719Z  INFO vector::topology::builder: Healthcheck: Passed.
2022-06-29T13:45:32.959733Z DEBUG vector::topology::running: Connecting inputs for sink. component=remap_console_sink
2022-06-29T13:45:32.959751Z  INFO vector::topology::builder: Healthcheck: Passed.
2022-06-29T13:45:32.959752Z DEBUG vector::topology::running: Adding component input to fanout. component=remap_console_sink fanout_id=remap
2022-06-29T13:45:32.959785Z DEBUG vector::topology::running: Spawning new source. key=logs
2022-06-29T13:45:32.959820Z DEBUG vector::topology::running: Spawning new transform. key=remap
2022-06-29T13:45:32.959866Z TRACE vector::topology::running: Spawning new sink. key=remap_console_dropped_sink
2022-06-29T13:45:32.959896Z TRACE vector::topology::running: Spawning new sink. key=remap_console_sink
2022-06-29T13:45:32.959886Z DEBUG source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector::topology::builder: Source pump starting.
2022-06-29T13:45:32.959982Z  INFO vector: Vector has started. debug="false" version="0.22.2" arch="x86_64" build_id="0024c92 2022-06-15"
2022-06-29T13:45:32.960021Z  INFO vector::app: API is disabled, enable by setting `api.enabled` to `true` and use commands like `vector top`.
2022-06-29T13:45:32.960710Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector::internal_events::common: Bytes received. byte_size=0 protocol=none
2022-06-29T13:45:32.960712Z DEBUG sink{component_kind="sink" component_id=remap_console_sink component_type=console component_name=remap_console_sink}: vector::utilization: utilization=0.012063242118913298
2022-06-29T13:45:32.960757Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector::internal_events::demo_logs: Received one event.
2022-06-29T13:45:32.960813Z DEBUG sink{component_kind="sink" component_id=remap_console_dropped_sink component_type=console component_name=remap_console_dropped_sink}: vector::utilization: utilization=0.04296335690125053
2022-06-29T13:45:32.960838Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_common::internal_event::events_received: Events received. count=1 byte_size=723
2022-06-29T13:45:32.960877Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-06-29T13:45:32.960896Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=416 output=_default
2022-06-29T13:45:32.960932Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_core::fanout: Processing control message outside of send: ControlMessage::Add(ComponentKey { id: "remap" })
2022-06-29T13:45:32.960962Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-06-29T13:45:32.960984Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_core::fanout: Sent item to fanout.
2022-06-29T13:45:32.961009Z TRACE transform{component_kind="transform" component_id=remap component_type=remap component_name=remap}: vector_common::internal_event::events_received: Events received. count=1 byte_size=416
2022-06-29T13:45:32.961103Z  INFO transform{component_kind="transform" component_id=remap component_type=remap component_name=remap}: vrl_stdlib::log: Processing value 'line' internal_log_rate_secs=0 vrl_position=46
2022-06-29T13:45:32.961127Z  INFO transform{component_kind="transform" component_id=remap component_type=remap component_name=remap}: vrl_stdlib::log: Processing value '2' internal_log_rate_secs=0 vrl_position=46
2022-06-29T13:45:32.961143Z  INFO transform{component_kind="transform" component_id=remap component_type=remap component_name=remap}: vrl_stdlib::log: Processing value 'abort' internal_log_rate_secs=0 vrl_position=46
thread 'vector-worker' panicked at 'abort errors must only be defined by `abort` statement', lib/vrl/compiler/src/expression/function_call.rs:577:17
stack backtrace:
2022-06-29T13:45:32.961812Z TRACE vector: Beep.
   0:     0x55e2db98b8dc - std::backtrace_rs::backtrace::libunwind::trace::h09f7e4e089375279
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/../../backtrace/src/backtrace/libunwind.rs:93:5
   1:     0x55e2db98b8dc - std::backtrace_rs::backtrace::trace_unsynchronized::h1ec96f1c7087094e
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/../../backtrace/src/backtrace/mod.rs:66:5
   2:     0x55e2db98b8dc - std::sys_common::backtrace::_print_fmt::h317b71fc9a5cf964
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:67:5
   3:     0x55e2db98b8dc - <std::sys_common::backtrace::_print::DisplayBacktrace as core::fmt::Display>::fmt::he3555b48e7dfe7f0
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:46:22
   4:     0x55e2db9e7cec - core::fmt::write::h513b07ca38f4fb1b
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/fmt/mod.rs:1149:17
   5:     0x55e2db97bb25 - std::io::Write::write_fmt::haf8c932b52111354
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/io/mod.rs:1697:15
   6:     0x55e2db98e980 - std::sys_common::backtrace::_print::h195c38364780a303
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:49:5
   7:     0x55e2db98e980 - std::sys_common::backtrace::print::hc09dfdea923b6730
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:36:9
   8:     0x55e2db98e980 - std::panicking::default_hook::{{closure}}::hb2e38ec0d91046a3
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:211:50
   9:     0x55e2db98e535 - std::panicking::default_hook::h60284635b0ad54a8
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:228:9
  10:     0x55e2db98f174 - std::panicking::rust_panic_with_hook::ha677a669fb275654
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:606:17
  11:     0x55e2db98ec22 - std::panicking::begin_panic_handler::{{closure}}::h976246fb95d93c31
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:500:13
  12:     0x55e2db98bd84 - std::sys_common::backtrace::__rust_end_short_backtrace::h38077ee5b7b9f99a
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:139:18
  13:     0x55e2db98ebb9 - rust_begin_unwind
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:498:5
  14:     0x55e2d6b55aa1 - core::panicking::panic_fmt::h35f3a62252ba0fd2
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/panicking.rs:107:14
  15:     0x55e2db0e23de - <vrl_compiler::expression::function_call::FunctionCall as vrl_compiler::expression::Expression>::resolve::h5b15fe8a1269adb9
  16:     0x55e2db0ed71f - <vrl_compiler::expression::Expr as vrl_compiler::expression::Expression>::resolve::hb535e71403c0621e
  17:     0x55e2db0cb667 - vrl_compiler::program::Program::resolve::h09656a71a1af82c8
  18:     0x55e2db06f833 - vrl::runtime::Runtime::resolve::h06a0cbf4de3b3196
  19:     0x55e2d85f16fa - <vector::transforms::remap::Remap<Runner> as vector_core::transform::SyncTransform>::transform::h793ceda3febf9c40
  20:     0x55e2d6ddf65e - vector_core::transform::SyncTransform::transform_all::hd3c0fb99c218e24e
  21:     0x55e2d758ba69 - tokio::runtime::task::harness::poll_future::h45279ef2e923948e
  22:     0x55e2d753b024 - tokio::runtime::task::raw::poll::ha66570bc77e7d949
  23:     0x55e2db5ad7de - tokio::runtime::thread_pool::worker::Context::run_task::h8e4a9d0f3cbe638d
  24:     0x55e2db5ace9b - tokio::runtime::thread_pool::worker::run::h28fe79c4911d1526
  25:     0x55e2db59d288 - tokio::runtime::task::raw::poll::h89d53825cf9e44ae
  26:     0x55e2db56da5b - std::sys_common::backtrace::__rust_begin_short_backtrace::h6348438fe675f738
  27:     0x55e2db5751f6 - core::ops::function::FnOnce::call_once{{vtable.shim}}::h90ebd4a050d2ce5c
  28:     0x55e2db99aa13 - <alloc::boxed::Box<F,A> as core::ops::function::FnOnce<Args>>::call_once::hcbc6d2d80772be64
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/alloc/src/boxed.rs:1694:9
  29:     0x55e2db99aa13 - <alloc::boxed::Box<F,A> as core::ops::function::FnOnce<Args>>::call_once::h9bffa2ca65a1d6e6
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/alloc/src/boxed.rs:1694:9
  30:     0x55e2db99aa13 - std::sys::unix::thread::Thread::new::thread_start::ha678a8b0caec8f55
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys/unix/thread.rs:106:17
  31:     0x7f254979a6db - start_thread
                               at /build/glibc-uZu3wS/glibc-2.27/nptl/pthread_create.c:463
  32:     0x7f254855e61f - clone
                               at /build/glibc-uZu3wS/glibc-2.27/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:95
  33:                0x0 - <unknown>
thread 'vector-worker' panicked at 'internal error: entered unreachable code: join error or bad poll', src/topology/builder.rs:669:30
stack backtrace:
   0:     0x55e2db98b8dc - std::backtrace_rs::backtrace::libunwind::trace::h09f7e4e089375279
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/../../backtrace/src/backtrace/libunwind.rs:93:5
   1:     0x55e2db98b8dc - std::backtrace_rs::backtrace::trace_unsynchronized::h1ec96f1c7087094e
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/../../backtrace/src/backtrace/mod.rs:66:5
   2:     0x55e2db98b8dc - std::sys_common::backtrace::_print_fmt::h317b71fc9a5cf964
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:67:5
   3:     0x55e2db98b8dc - <std::sys_common::backtrace::_print::DisplayBacktrace as core::fmt::Display>::fmt::he3555b48e7dfe7f0
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:46:22
   4:     0x55e2db9e7cec - core::fmt::write::h513b07ca38f4fb1b
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/fmt/mod.rs:1149:17
   5:     0x55e2db97bb25 - std::io::Write::write_fmt::haf8c932b52111354
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/io/mod.rs:1697:15
   6:     0x55e2db98e980 - std::sys_common::backtrace::_print::h195c38364780a303
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:49:5
   7:     0x55e2db98e980 - std::sys_common::backtrace::print::hc09dfdea923b6730
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:36:9
   8:     0x55e2db98e980 - std::panicking::default_hook::{{closure}}::hb2e38ec0d91046a3
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:211:50
   9:     0x55e2db98e535 - std::panicking::default_hook::h60284635b0ad54a8
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:228:9
  10:     0x55e2db98f174 - std::panicking::rust_panic_with_hook::ha677a669fb275654
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:606:17
  11:     0x55e2db98ec50 - std::panicking::begin_panic_handler::{{closure}}::h976246fb95d93c31
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:502:13
  12:     0x55e2db98bd84 - std::sys_common::backtrace::__rust_end_short_backtrace::h38077ee5b7b9f99a
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:139:18
  13:     0x55e2db98ebb9 - rust_begin_unwind
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:498:5
  14:     0x55e2d6b55aa1 - core::panicking::panic_fmt::h35f3a62252ba0fd2
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/panicking.rs:107:14
  15:     0x55e2d7ded260 - <core::future::from_generator::GenFuture<T> as core::future::future::Future>::poll::h233001bc763e540a
  16:     0x55e2d767ed11 - <core::pin::Pin<P> as core::future::future::Future>::poll::h510bfb84ee7a5b0e
  17:     0x55e2d7589916 - tokio::runtime::task::harness::poll_future::h412825b75e959fcd
  18:     0x55e2d753294b - tokio::runtime::task::raw::poll::h585d9b181785f0cb
  19:     0x55e2db5ad7de - tokio::runtime::thread_pool::worker::Context::run_task::h8e4a9d0f3cbe638d
  20:     0x55e2db5ace9b - tokio::runtime::thread_pool::worker::run::h28fe79c4911d1526
  21:     0x55e2db59d288 - tokio::runtime::task::raw::poll::h89d53825cf9e44ae
  22:     0x55e2db56da5b - std::sys_common::backtrace::__rust_begin_short_backtrace::h6348438fe675f738
  23:     0x55e2db5751f6 - core::ops::function::FnOnce::call_once{{vtable.shim}}::h90ebd4a050d2ce5c
  24:     0x55e2db99aa13 - <alloc::boxed::Box<F,A> as core::ops::function::FnOnce<Args>>::call_once::hcbc6d2d80772be64
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/alloc/src/boxed.rs:1694:9
  25:     0x55e2db99aa13 - <alloc::boxed::Box<F,A> as core::ops::function::FnOnce<Args>>::call_once::h9bffa2ca65a1d6e6
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/alloc/src/boxed.rs:1694:9
  26:     0x55e2db99aa13 - std::sys::unix::thread::Thread::new::thread_start::ha678a8b0caec8f55
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys/unix/thread.rs:106:17
  27:     0x7f254979a6db - start_thread
                               at /build/glibc-uZu3wS/glibc-2.27/nptl/pthread_create.c:463
  28:     0x7f254855e61f - clone
                               at /build/glibc-uZu3wS/glibc-2.27/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:95
  29:                0x0 - <unknown>
2022-06-29T13:45:33.018884Z ERROR transform{component_kind="transform" component_id=remap component_type=remap component_name=remap}: vector::topology: An error occurred that Vector couldn't handle.
2022-06-29T13:45:33.019473Z  INFO vector: Vector has stopped.
2022-06-29T13:45:33.019552Z DEBUG sink{component_kind="sink" component_id=remap_console_dropped_sink component_type=console component_name=remap_console_dropped_sink}: vector::topology::builder: Finished.
2022-06-29T13:45:33.019554Z DEBUG sink{component_kind="sink" component_id=remap_console_sink component_type=console component_name=remap_console_sink}: vector::topology::builder: Finished.
2022-06-29T13:45:33.020621Z  INFO vector::topology::running: Shutting down... Waiting on running components. remaining_components="logs" time_remaining="59 seconds left"
2022-06-29T13:45:33.961000Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector::internal_events::common: Bytes received. byte_size=0 protocol=none
2022-06-29T13:45:33.961107Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector::internal_events::demo_logs: Received one event.
2022-06-29T13:45:33.961256Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_common::internal_event::events_received: Events received. count=1 byte_size=723
2022-06-29T13:45:33.961346Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_buffers::topology::channel::limited_queue: Sent item.
2022-06-29T13:45:33.961389Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_common::internal_event::events_sent: Events sent. count=1 byte_size=416 output=_default
2022-06-29T13:45:33.961474Z DEBUG source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector::topology::builder: Finished.
2022-06-29T13:45:33.961588Z TRACE source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector_core::fanout: Processing control message inside of send: None
thread 'vector-worker' panicked at 'unit error: ()', lib/vector-core/src/fanout.rs:369:42
stack backtrace:
   0:     0x55e2db98b8dc - std::backtrace_rs::backtrace::libunwind::trace::h09f7e4e089375279
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/../../backtrace/src/backtrace/libunwind.rs:93:5
   1:     0x55e2db98b8dc - std::backtrace_rs::backtrace::trace_unsynchronized::h1ec96f1c7087094e
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/../../backtrace/src/backtrace/mod.rs:66:5
   2:     0x55e2db98b8dc - std::sys_common::backtrace::_print_fmt::h317b71fc9a5cf964
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:67:5
   3:     0x55e2db98b8dc - <std::sys_common::backtrace::_print::DisplayBacktrace as core::fmt::Display>::fmt::he3555b48e7dfe7f0
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:46:22
   4:     0x55e2db9e7cec - core::fmt::write::h513b07ca38f4fb1b
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/fmt/mod.rs:1149:17
   5:     0x55e2db97bb25 - std::io::Write::write_fmt::haf8c932b52111354
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/io/mod.rs:1697:15
   6:     0x55e2db98e980 - std::sys_common::backtrace::_print::h195c38364780a303
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:49:5
   7:     0x55e2db98e980 - std::sys_common::backtrace::print::hc09dfdea923b6730
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:36:9
   8:     0x55e2db98e980 - std::panicking::default_hook::{{closure}}::hb2e38ec0d91046a3
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:211:50
   9:     0x55e2db98e535 - std::panicking::default_hook::h60284635b0ad54a8
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:228:9
  10:     0x55e2db98f174 - std::panicking::rust_panic_with_hook::ha677a669fb275654
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:606:17
  11:     0x55e2db98ec50 - std::panicking::begin_panic_handler::{{closure}}::h976246fb95d93c31
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:502:13
  12:     0x55e2db98bd84 - std::sys_common::backtrace::__rust_end_short_backtrace::h38077ee5b7b9f99a
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:139:18
  13:     0x55e2db98ebb9 - rust_begin_unwind
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:498:5
  14:     0x55e2d6b55aa1 - core::panicking::panic_fmt::h35f3a62252ba0fd2
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/panicking.rs:107:14
  15:     0x55e2d6b55b93 - core::result::unwrap_failed::hb53671404b9e33c2
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/result.rs:1613:5
  16:     0x55e2daf77f6d - <core::future::from_generator::GenFuture<T> as core::future::future::Future>::poll::h6bc8339f16b6be09
  17:     0x55e2d7ef02d3 - <core::future::from_generator::GenFuture<T> as core::future::future::Future>::poll::h7142bef86bae173b
  18:     0x55e2d7580483 - tokio::runtime::task::harness::poll_future::h1bde4adc2e60af4b
  19:     0x55e2d7532aec - tokio::runtime::task::raw::poll::h5ab34974d6bf6bdb
  20:     0x55e2db5ad7de - tokio::runtime::thread_pool::worker::Context::run_task::h8e4a9d0f3cbe638d
  21:     0x55e2db5aca07 - tokio::runtime::thread_pool::worker::run::h28fe79c4911d1526
  22:     0x55e2db59d288 - tokio::runtime::task::raw::poll::h89d53825cf9e44ae
  23:     0x55e2db56da5b - std::sys_common::backtrace::__rust_begin_short_backtrace::h6348438fe675f738
  24:     0x55e2db5751f6 - core::ops::function::FnOnce::call_once{{vtable.shim}}::h90ebd4a050d2ce5c
  25:     0x55e2db99aa13 - <alloc::boxed::Box<F,A> as core::ops::function::FnOnce<Args>>::call_once::hcbc6d2d80772be64
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/alloc/src/boxed.rs:1694:9
  26:     0x55e2db99aa13 - <alloc::boxed::Box<F,A> as core::ops::function::FnOnce<Args>>::call_once::h9bffa2ca65a1d6e6
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/alloc/src/boxed.rs:1694:9
  27:     0x55e2db99aa13 - std::sys::unix::thread::Thread::new::thread_start::ha678a8b0caec8f55
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys/unix/thread.rs:106:17
  28:     0x7f254979a6db - start_thread
                               at /build/glibc-uZu3wS/glibc-2.27/nptl/pthread_create.c:463
  29:     0x7f254855e61f - clone
                               at /build/glibc-uZu3wS/glibc-2.27/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:95
  30:                0x0 - <unknown>
thread 'vector-worker' panicked at 'join error: JoinError::Panic(Id(15), ...)', src/topology/builder.rs:212:30
stack backtrace:
   0:     0x55e2db98b8dc - std::backtrace_rs::backtrace::libunwind::trace::h09f7e4e089375279
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/../../backtrace/src/backtrace/libunwind.rs:93:5
   1:     0x55e2db98b8dc - std::backtrace_rs::backtrace::trace_unsynchronized::h1ec96f1c7087094e
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/../../backtrace/src/backtrace/mod.rs:66:5
   2:     0x55e2db98b8dc - std::sys_common::backtrace::_print_fmt::h317b71fc9a5cf964
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:67:5
   3:     0x55e2db98b8dc - <std::sys_common::backtrace::_print::DisplayBacktrace as core::fmt::Display>::fmt::he3555b48e7dfe7f0
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:46:22
   4:     0x55e2db9e7cec - core::fmt::write::h513b07ca38f4fb1b
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/fmt/mod.rs:1149:17
   5:     0x55e2db97bb25 - std::io::Write::write_fmt::haf8c932b52111354
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/io/mod.rs:1697:15
   6:     0x55e2db98e980 - std::sys_common::backtrace::_print::h195c38364780a303
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:49:5
   7:     0x55e2db98e980 - std::sys_common::backtrace::print::hc09dfdea923b6730
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:36:9
   8:     0x55e2db98e980 - std::panicking::default_hook::{{closure}}::hb2e38ec0d91046a3
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:211:50
   9:     0x55e2db98e535 - std::panicking::default_hook::h60284635b0ad54a8
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:228:9
  10:     0x55e2db98f174 - std::panicking::rust_panic_with_hook::ha677a669fb275654
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:606:17
  11:     0x55e2db98ec50 - std::panicking::begin_panic_handler::{{closure}}::h976246fb95d93c31
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:502:13
  12:     0x55e2db98bd84 - std::sys_common::backtrace::__rust_end_short_backtrace::h38077ee5b7b9f99a
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys_common/backtrace.rs:139:18
  13:     0x55e2db98ebb9 - rust_begin_unwind
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/panicking.rs:498:5
  14:     0x55e2d6b55aa1 - core::panicking::panic_fmt::h35f3a62252ba0fd2
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/panicking.rs:107:14
  15:     0x55e2d6b55b93 - core::result::unwrap_failed::hb53671404b9e33c2
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/core/src/result.rs:1613:5
  16:     0x55e2d7e03639 - <core::future::from_generator::GenFuture<T> as core::future::future::Future>::poll::h2d65545dc8fde948
  17:     0x55e2d7589916 - tokio::runtime::task::harness::poll_future::h412825b75e959fcd
  18:     0x55e2d753294b - tokio::runtime::task::raw::poll::h585d9b181785f0cb
  19:     0x55e2db5ad7de - tokio::runtime::thread_pool::worker::Context::run_task::h8e4a9d0f3cbe638d
  20:     0x55e2db5aca07 - tokio::runtime::thread_pool::worker::run::h28fe79c4911d1526
  21:     0x55e2db59d288 - tokio::runtime::task::raw::poll::h89d53825cf9e44ae
  22:     0x55e2db56da5b - std::sys_common::backtrace::__rust_begin_short_backtrace::h6348438fe675f738
  23:     0x55e2db5751f6 - core::ops::function::FnOnce::call_once{{vtable.shim}}::h90ebd4a050d2ce5c
  24:     0x55e2db99aa13 - <alloc::boxed::Box<F,A> as core::ops::function::FnOnce<Args>>::call_once::hcbc6d2d80772be64
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/alloc/src/boxed.rs:1694:9
  25:     0x55e2db99aa13 - <alloc::boxed::Box<F,A> as core::ops::function::FnOnce<Args>>::call_once::h9bffa2ca65a1d6e6
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/alloc/src/boxed.rs:1694:9
  26:     0x55e2db99aa13 - std::sys::unix::thread::Thread::new::thread_start::ha678a8b0caec8f55
                               at /rustc/db9d1b20bba1968c1ec1fc49616d4742c1725b4b/library/std/src/sys/unix/thread.rs:106:17
  27:     0x7f254979a6db - start_thread
                               at /build/glibc-uZu3wS/glibc-2.27/nptl/pthread_create.c:463
  28:     0x7f254855e61f - clone
                               at /build/glibc-uZu3wS/glibc-2.27/misc/../sysdeps/unix/sysv/linux/x86_64/clone.S:95
  29:                0x0 - <unknown>
2022-06-29T13:45:33.970922Z ERROR source{component_kind="source" component_id=logs component_type=demo_logs component_name=logs}: vector::topology: An error occurred that Vector couldn't handle.
2022-06-29T13:45:33.970981Z TRACE vector: Beep.
```


### Example Data

See config provided.

### Additional Context

_No response_

### References

Maybe the same problem reported in vectordotdev/vector#13010
