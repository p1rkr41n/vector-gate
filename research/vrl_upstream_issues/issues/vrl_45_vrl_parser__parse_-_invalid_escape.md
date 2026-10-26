# [#45] vrl_parser::parse - invalid escape

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/45)
- **Status**: `OPEN`
- **Author**: [@stasos24](https://github.com/stasos24)
- **Created At**: `2022-07-13T06:18:21Z`
- **Updated At**: `2026-06-01T14:05:44Z`
- **Comments**: 0
- **Labels**: `vrl:parser`, `fuzz`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/45)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

vrl_parser::parser function panics when receive a crash.file input
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
thread 'main' panicked at 'not implemented: invalid escape', /opt/fuzz/vector/lib/vrl/parser/src/lex.rs:1266:22
stack backtrace:
   0: rust_begin_unwind
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/std/src/panicking.rs:584:5
   1: core::panicking::panic_fmt
             at /rustc/38b72154ded23847cd08a796d0c6708b5efac265/library/core/src/panicking.rs:142:14
   2: vrl_parser::lex::unescape_string_literal
   3: vrl_parser::lex::StringLiteralToken<&str>::template
   4: vrl_parser::parser::__parse__Program::__reduce494
   5: vrl_parser::parser::__parse__Program::__reduce
   6: <vrl_parser::parser::__parse__Program::__StateMachine as lalrpop_util::state_machine::ParserDefinition>::reduce
   7: covbuild::main
```


### Example Data
[crash_file](https://github.com/stasos24/vector_crash_files/blob/main/crash_escape.file)
VRL Source:
`"\}"n"`
### Additional Context

_No response_

### References

_No response_
