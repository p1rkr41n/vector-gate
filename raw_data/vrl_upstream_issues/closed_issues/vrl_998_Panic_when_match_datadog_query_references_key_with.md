# Issue #998: Panic when match_datadog_query references key with hyphen

- **URL:** https://github.com/vectordotdev/vrl/issues/998
- **Author:** @dekelpilli
- **Status:** CLOSED (completed)
- **Created:** 2024-08-20T04:18:39Z
- **Closed:** 2024-09-10T14:24:22Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

`match_datadog_query` cannot handle keys with hyphens in them. For example:
```
.custom."abc_def" = true
exists = match_datadog_query(., "_exists_:@abc_def") #works as expected, returns true

.custom."abc-def" = true
exists = match_datadog_query(., "_exists_:@abc-def") # panics, regardless of it key exists
```

### Configuration

```text
Reproducible from VRL REPL
```


### Version

vector 0.40.0 (x86_64-apple-darwin 1167aa9 2024-07-29 15:08:44.028365803)

### Debug Output

```text
thread 'main' panicked at /Users/runner/.cargo/registry/src/index.crates.io-6f17d22bba15001f/vrl-0.17.0/src/stdlib/match_datadog_query.rs:418:42:
should parse value path (lookup_field): InvalidPathSyntax { path: "custom.abc-def" }
stack backtrace:
   0: _rust_begin_unwind
   1: core::panicking::panic_fmt
   2: core::result::unwrap_failed
   3: vrl::stdlib::match_datadog_query::lookup_field
   4: <vrl::stdlib::match_datadog_query::VrlFilter as vrl::datadog::filter::filter::Filter<vrl::value::value::Value>>::exists
   5: vrl::datadog::filter::matcher::build_matcher
   6: <vrl::stdlib::match_datadog_query::MatchDatadogQuery as vrl::compiler::function::Function>::compile
   7: vrl::compiler::compiler::Compiler::compile_function_call
   8: vrl::compiler::compiler::Compiler::compile_expr
   9: vrl::compiler::compile_with_state
  10: vrl::cli::repl::resolve
  11: <vrl::cli::repl::Repl as rustyline::validate::Validator>::validate
  12: rustyline::Editor<H,I>::readline_edit
  13: vrl::cli::cmd::run
  14: vrl::cli::cmd::cmd
  15: vector::cli::SubCommand::execute::{{closure}}
  16: vector::app::Application::prepare_from_opts
  17: vector::app::Application::run
  18: vector::main
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.
```


### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
