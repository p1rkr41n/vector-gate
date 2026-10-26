# Issue #46:  vrl::compile: attempt to subtract with overflow

- **URL:** https://github.com/vectordotdev/vrl/issues/46
- **Author:** @stasos24
- **Status:** CLOSED (completed)
- **Created:** 2022-07-13T06:03:47Z
- **Closed:** 2023-04-28T17:28:17Z
- **Labels:** vrl:compiler, fuzz

## Description

Hello, i've found a secureity bug during fuzzing vector.

Version: v0.23.0

Steps to reproduce:
Download a repo with fuzz harness: https://github.com/stasos24/vector/tree/master/lib/vrl/core/fuzzing
```
cargo build --bin covbuild
target/debug/covbuild < crash.file
```
Link to crash.file:
[crash_file](https://github.com/stasos24/vector_crash_files/blob/main/crash.file)

Rust backtrace:
```
thread 'main' panicked at 'attempt to subtract with overflow', /opt/fuzz/vector/lib/vrl/compiler/src/expression/assignment.rs:250:37
stack backtrace:
   0: rust_begin_unwind
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/std/src/panicking.rs:584:5
   1: core::panicking::panic_fmt
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/core/src/panicking.rs:142:14
   2: core::panicking::panic
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/core/src/panicking.rs:48:5
   3: vrl_compiler::expression::assignment::verify_overwriteable
             at /opt/fuzz/vector/lib/vrl/compiler/src/expression/assignment.rs:250:37
   4: vrl_compiler::expression::assignment::Assignment::new
             at /opt/fuzz/vector/lib/vrl/compiler/src/expression/assignment.rs:64:17
   5: vrl_compiler::compiler::Compiler::compile_assignment
             at /opt/fuzz/vector/lib/vrl/compiler/src/compiler.rs:551:26
   6: vrl_compiler::compiler::Compiler::compile_expr
             at /opt/fuzz/vector/lib/vrl/compiler/src/compiler.rs:118:33
   7: vrl_compiler::compiler::Compiler::compile_root_exprs
             at /opt/fuzz/vector/lib/vrl/compiler/src/compiler.rs:231:41
   8: vrl_compiler::compiler::Compiler::compile
             at /opt/fuzz/vector/lib/vrl/compiler/src/compiler.rs:61:27
   9: vrl::compile_with_state
             at /opt/fuzz/vector/lib/vrl/vrl/src/lib.rs:45:5
  10: vrl::compile_with_external
             at /opt/fuzz/vector/lib/vrl/vrl/src/lib.rs:34:5
  11: vrl::compile
             at /opt/fuzz/vector/lib/vrl/vrl/src/lib.rs:26:5
  12: covbuild::main
             at ./src/cov.rs:14:3
  13: core::ops::function::FnOnce::call_once
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/core/src/ops/function.rs:248:5
```

