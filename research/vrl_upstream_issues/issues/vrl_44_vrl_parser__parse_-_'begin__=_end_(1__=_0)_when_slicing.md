# [#44] vrl_parser::parse - 'begin <= end (1 <= 0) when slicing

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/44)
- **Status**: `OPEN`
- **Author**: [@stasos24](https://github.com/stasos24)
- **Created At**: `2022-07-13T06:25:49Z`
- **Updated At**: `2026-06-01T14:05:46Z`
- **Comments**: 1
- **Labels**: `vrl:parser`, `fuzz`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/44)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

vrl_parser::parser function panics when receive a crash_slice.file input
Steps to reproduce:
Download a repo with fuzz harness: https://github.com/stasos24/vector/tree/master/lib/vrl/parser/fuzzing
```
cargo build --bin covbuild
target/debug/covbuild < crash_escape.file
```

### Configuration

_No response_

### Version

v0.23.0

### Debug Output

```text
thread 'main' panicked at 'begin <= end (1 <= 0) when slicing `"`', library/core/src/str/mod.rs:111:5
stack backtrace:
   0: rust_begin_unwind
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/std/src/panicking.rs:584:5
   1: core::panicking::panic_fmt
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/core/src/panicking.rs:142:14
   2: core::str::slice_error_fail_rt
   3: core::ops::function::FnOnce::call_once
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/core/src/ops/function.rs:248:5
   4: core::intrinsics::const_eval_select
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/core/src/intrinsics.rs:2695:5
   5: core::str::slice_error_fail
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/core/src/str/mod.rs:86:9
   6: <lookup::lookup_buf::segmentbuf::FieldBuf as core::convert::From<alloc::string::String>>::from
   7: vrl_parser::parser::__action78
   8: vrl_parser::parser::__parse__Program::__reduce245
   9: vrl_parser::parser::__parse__Program::__reduce
  10: <vrl_parser::parser::__parse__Program::__StateMachine as lalrpop_util::state_machine::ParserDefinition>::reduce
  11: covbuild::main
```


### Example Data

[crash_file](https://github.com/stasos24/vector_crash_files/blob/main/crash_slice.file)

VRL source:
`.s"Ws{g+  AB_3.""\"_3.""\""""`
### Additional Context

_No response_

### References

_No response_
