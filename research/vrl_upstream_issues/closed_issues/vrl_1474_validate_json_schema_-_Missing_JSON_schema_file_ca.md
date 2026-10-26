# Issue #1474: `validate_json_schema` - Missing JSON schema file causes panic

- **URL:** https://github.com/vectordotdev/vrl/issues/1474
- **Author:** @sbalmos
- **Status:** CLOSED (completed)
- **Created:** 2025-08-13T20:04:37Z
- **Closed:** 2025-08-28T17:36:35Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

The implementation of `validate_json_schema` requires that the referenced JSON schema file be accessible _at function call compile time_, rather than merely at runtime / evaluation time. If the given JSON schema file path is inaccessible, VRL and Vector will panic, causing a total app crash.

I believe the intention would be to merely throw a VRL function error at runtime.

### VRL Program

```text
valid, err = validate_json_schema(s'{"hi":1}', "some/bad/path/json-schema.json")
```

### VRL and/or Vector Version

VRL 0.26 in Vector 0.49

### Debug Output

```text
$ valid, err = validate_json_schema(s'{"hi":1}', "some/bad/path/json-schema.json")
thread 'main' panicked at src/stdlib/validate_json_schema.rs:83:56:
JSON schema not found: "Failed to open schema definition file 'some/bad/path/json-schema.json': No such file or directory (os error 2)"
stack backtrace:
   0: __rustc::rust_begin_unwind
             at /rustc/6b00bc3880198600130e1cf62b8f8a93494488cc/library/std/src/panicking.rs:697:5
   1: core::panicking::panic_fmt
             at /rustc/6b00bc3880198600130e1cf62b8f8a93494488cc/library/core/src/panicking.rs:75:14
   2: core::result::unwrap_failed
             at /rustc/6b00bc3880198600130e1cf62b8f8a93494488cc/library/core/src/result.rs:1732:5
   3: core::result::Result<T,E>::expect
             at /home/sbalmos/.rustup/toolchains/1.88-x86_64-unknown-linux-gnu/lib/rustlib/src/rust/library/core/src/result.rs:1089:23
   4: <vrl::stdlib::validate_json_schema::ValidateJsonSchema as vrl::compiler::function::Function>::compile
             at ./src/stdlib/validate_json_schema.rs:83:13
   5: vrl::compiler::expression::function_call::Builder::compile
             at ./src/compiler/expression/function_call.rs:419:20
   6: vrl::compiler::compiler::Compiler::compile_function_call::{{closure}}
             at ./src/compiler/compiler.rs:741:13
   7: core::option::Option<T>::and_then
             at /home/sbalmos/.rustup/toolchains/1.88-x86_64-unknown-linux-gnu/lib/rustlib/src/rust/library/core/src/option.rs:1477:24
   8: vrl::compiler::compiler::Compiler::compile_function_call
             at ./src/compiler/compiler.rs:713:29
   9: vrl::compiler::compiler::Compiler::compile_expr
             at ./src/compiler/compiler.rs:179:35
  10: vrl::compiler::compiler::Compiler::compile_assignment
             at ./src/compiler/compiler.rs:525:36
  11: vrl::compiler::compiler::Compiler::compile_expr
             at ./src/compiler/compiler.rs:177:33
  12: vrl::compiler::compiler::Compiler::compile_root_exprs
             at ./src/compiler/compiler.rs:287:41
  13: vrl::compiler::compiler::Compiler::compile
             at ./src/compiler/compiler.rs:120:27
  14: vrl::compiler::compile_with_state
             at ./src/compiler/mod.rs:142:18
  15: vrl::cli::repl::resolve
             at ./src/cli/repl.rs:172:25
  16: <vrl::cli::repl::Repl as rustyline::validate::Validator>::validate
             at ./src/cli/repl.rs:304:22
  17: rustyline::edit::State<H>::validate
             at /home/sbalmos/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rustyline-16.0.0/src/edit.rs:240:26
  18: rustyline::command::execute
             at /home/sbalmos/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rustyline-16.0.0/src/command.rs:133:37
  19: rustyline::Editor<H,I>::readline_edit
             at /home/sbalmos/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rustyline-16.0.0/src/lib.rs:784:19
  20: rustyline::Editor<H,I>::readline_with
             at /home/sbalmos/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rustyline-16.0.0/src/lib.rs:664:30
  21: rustyline::Editor<H,I>::readline
             at /home/sbalmos/.cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rustyline-16.0.0/src/lib.rs:638:9
  22: vrl::cli::repl::run
             at ./src/cli/repl.rs:76:24
  23: vrl::cli::cmd::repl
             at ./src/cli/cmd.rs:206:5
  24: vrl::cli::cmd::run
             at ./src/cli/cmd.rs:126:9
  25: vrl::cli::cmd::cmd
             at ./src/cli/cmd.rs:102:11
  26: vrl::main
             at ./lib/cli/src/main.rs:5:24
  27: core::ops::function::FnOnce::call_once
             at /home/sbalmos/.rustup/toolchains/1.88-x86_64-unknown-linux-gnu/lib/rustlib/src/rust/library/core/src/ops/function.rs:250:5
note: Some details are omitted, run with `RUST_BACKTRACE=full` for a verbose backtrace.

Process finished with exit code 101
```

### Example

_No response_

### Additional Context

The issue(s) seem to lie in that the check for a valid path is during the `compile` phase of the `ValidateJsonSchema` `Function` impl, at https://github.com/vectordotdev/vrl/blob/main/src/stdlib/validate_json_schema.rs#L81-L83. This call to `get_json_schema_definition` should probably be moved into the runtime evaluation phase, in the `resolve` `FunctionExpression` impl of `ValidateSchemaJsonFn`, and return an Error if the schema cannot be loaded.

### References

_No response_
