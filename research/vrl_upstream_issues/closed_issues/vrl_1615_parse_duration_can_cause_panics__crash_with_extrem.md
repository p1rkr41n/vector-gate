# Issue #1615: `parse_duration` can cause panics & crash with extreme values

- **URL:** https://github.com/vectordotdev/vrl/issues/1615
- **Author:** @srstrickland
- **Status:** CLOSED (completed)
- **Created:** 2026-01-28T06:11:52Z
- **Closed:** 2026-02-02T18:12:51Z
- **Labels:** stdlib:parse_duration

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

When given somewhat nonsensical values, `parse_duration` can cause panics in vector and crash the process.  Attempting to parse those values should fail, but not cause the process to die.  Below is a simple repro using vector 0.52.0:

```
$ vector --version
vector 0.52.0 (x86_64-unknown-linux-gnu ca5bf26 2025-12-16 14:56:07.290167996)

$ vector vrl
<snip>

$ parse_duration!("123456789012345678901234d", "s")
10666666570666668000000000000

$ parse_duration!("1234567890123456789012345d", "s")
thread 'main' (803763) panicked at /cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rust_decimal-1.39.0/src/arithmetic_impls.rs:232:18:
Multiplication overflowed
stack backtrace:
   0:     0x558eee73aafa - <std::sys::backtrace::BacktraceLock::print::DisplayBacktrace as core::fmt::Display>::fmt::haa87a551a4affa55
   1:     0x558eed8477ef - core::fmt::write::h80461e1e45e4fdd2
   2:     0x558eee73a56f - std::io::Write::write_fmt::h6e6c69b2d6337d9b
   3:     0x558eee73a8d3 - std::sys::backtrace::BacktraceLock::print::hf67a46baa621998e
   4:     0x558eee73a00c - std::panicking::panic_with_hook::h185ddfb86bf14d73
   5:     0x558eee760df5 - std::panicking::panic_handler::{{closure}}::had89ddd01b6112c9
   6:     0x558eee760d89 - std::sys::backtrace::__rust_end_short_backtrace::h5d0fc36eef7265ea
   7:     0x558eee760d7c - __rustc[eb8946e36839644a]::rust_begin_unwind
   8:     0x558eecddc9df - core::panicking::panic_fmt::h92c8e5abe71dd8d1
   9:     0x558ef1c55925 - <vrl::compiler::expression::function::FunctionExpressionAdapter<T> as vrl::compiler::expression::Expression>::resolve::h419bb49eeea81efe
  10:     0x558ef181577a - <vrl::compiler::expression::function_call::FunctionCall as vrl::compiler::expression::Expression>::resolve::h45ab5642d435a600
  11:     0x558ef17ee6e5 - <vrl::compiler::expression::Expr as vrl::compiler::expression::Expression>::resolve::h77ddf36d18a50e20
  12:     0x558ef1b082ba - vrl::compiler::runtime::Runtime::resolve::h2c9c318d72fe5cc9
  13:     0x558ef1b100c4 - vrl::cli::repl::resolve::hf35e6639d1a04614
  14:     0x558ef1b1f1e0 - <vrl::cli::repl::Repl as rustyline::validate::Validator>::validate::h84ccb0f0c9099faf
  15:     0x558ef1b195f2 - rustyline::edit::State<H>::validate::he380d05a0612cc4f
  16:     0x558ef1b0b02d - rustyline::Editor<H,I>::readline_edit::hb25f290df8c7cb50
  17:     0x558ef1af9d12 - vrl::cli::cmd::run::h82eba3f13ec0c79c
  18:     0x558ef1af6a4b - vrl::cli::cmd::cmd::h807dc6066ee01ee3
  19:     0x558ef12b4f8c - vector::cli::SubCommand::execute::{{closure}}::heabb6e53e8ff0e22
  20:     0x558ef12ad2e4 - vector::app::Application::prepare_from_opts::hd6cbf0283de971c6
  21:     0x558ef14c995e - vector::app::Application::run::h55485fc0b2f041c6
  22:     0x558eecef32d3 - vector::main::hfa40d1e263d4a099
  23:     0x558eecef1633 - std::sys::backtrace::__rust_begin_short_backtrace::h77e51ffc337dd002
  24:     0x558eecef4081 - main
  25:     0x7f27f216e083 - __libc_start_main
                               at /build/glibc-B3wQXB/glibc-2.31/csu/../csu/libc-start.c:308:16
  26:     0x558eecef1529 - _start
  27:                0x0 - <unknown>
```

In our case, we were using `parse_duration` (probably overzealously) in a section of code that generically tries to transform arbitrary strings into "better" values by just attempting a few things:

```
typed = map_values(object(parsed), recursive: true) -> |value| {
  parse_int(value) ?? parse_float(value) ?? parse_duration(value, "s") ?? value
}
```

After years of stability, seemingly out of nowhere, our entire fleet went down, presumably after receiving a bunch of logs which had fields that would crash `parse_duration` as the value above does.  It wasn't trivial to determine the source but once we did it was fairly easy to reproduce.

### VRL Program

```text
typed = map_values(object(parsed), recursive: true) -> |value| {
  parse_int(value) ?? parse_float(value) ?? parse_duration(value, "s") ?? value
}
```

### VRL and/or Vector Version

vector 0.52.0 (x86_64-unknown-linux-gnu ca5bf26 2025-12-16 14:56:07.290167996)

### Debug Output

```text
$ parse_duration!("1234567890123456789012345d", "s")
thread 'main' (803763) panicked at /cargo/registry/src/index.crates.io-1949cf8c6b5b557f/rust_decimal-1.39.0/src/arithmetic_impls.rs:232:18:
Multiplication overflowed
stack backtrace:
   0:     0x558eee73aafa - <std::sys::backtrace::BacktraceLock::print::DisplayBacktrace as core::fmt::Display>::fmt::haa87a551a4affa55
   1:     0x558eed8477ef - core::fmt::write::h80461e1e45e4fdd2
   2:     0x558eee73a56f - std::io::Write::write_fmt::h6e6c69b2d6337d9b
   3:     0x558eee73a8d3 - std::sys::backtrace::BacktraceLock::print::hf67a46baa621998e
   4:     0x558eee73a00c - std::panicking::panic_with_hook::h185ddfb86bf14d73
   5:     0x558eee760df5 - std::panicking::panic_handler::{{closure}}::had89ddd01b6112c9
   6:     0x558eee760d89 - std::sys::backtrace::__rust_end_short_backtrace::h5d0fc36eef7265ea
   7:     0x558eee760d7c - __rustc[eb8946e36839644a]::rust_begin_unwind
   8:     0x558eecddc9df - core::panicking::panic_fmt::h92c8e5abe71dd8d1
   9:     0x558ef1c55925 - <vrl::compiler::expression::function::FunctionExpressionAdapter<T> as vrl::compiler::expression::Expression>::resolve::h419bb49eeea81efe
  10:     0x558ef181577a - <vrl::compiler::expression::function_call::FunctionCall as vrl::compiler::expression::Expression>::resolve::h45ab5642d435a600
  11:     0x558ef17ee6e5 - <vrl::compiler::expression::Expr as vrl::compiler::expression::Expression>::resolve::h77ddf36d18a50e20
  12:     0x558ef1b082ba - vrl::compiler::runtime::Runtime::resolve::h2c9c318d72fe5cc9
  13:     0x558ef1b100c4 - vrl::cli::repl::resolve::hf35e6639d1a04614
  14:     0x558ef1b1f1e0 - <vrl::cli::repl::Repl as rustyline::validate::Validator>::validate::h84ccb0f0c9099faf
  15:     0x558ef1b195f2 - rustyline::edit::State<H>::validate::he380d05a0612cc4f
  16:     0x558ef1b0b02d - rustyline::Editor<H,I>::readline_edit::hb25f290df8c7cb50
  17:     0x558ef1af9d12 - vrl::cli::cmd::run::h82eba3f13ec0c79c
  18:     0x558ef1af6a4b - vrl::cli::cmd::cmd::h807dc6066ee01ee3
  19:     0x558ef12b4f8c - vector::cli::SubCommand::execute::{{closure}}::heabb6e53e8ff0e22
  20:     0x558ef12ad2e4 - vector::app::Application::prepare_from_opts::hd6cbf0283de971c6
  21:     0x558ef14c995e - vector::app::Application::run::h55485fc0b2f041c6
  22:     0x558eecef32d3 - vector::main::hfa40d1e263d4a099
  23:     0x558eecef1633 - std::sys::backtrace::__rust_begin_short_backtrace::h77e51ffc337dd002
  24:     0x558eecef4081 - main
  25:     0x7f27f216e083 - __libc_start_main
                               at /build/glibc-B3wQXB/glibc-2.31/csu/../csu/libc-start.c:308:16
  26:     0x558eecef1529 - _start
  27:                0x0 - <unknown>
```

### Example

slides under the radar: https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLnBhcnNlZCA9IHBhcnNlX2R1cmF0aW9uISguYmFkLCBcInNcIikiLCJldmVudCI6eyJiYWQiOiIxMjM0NTY3ODkwMTIzNDU2Nzg5MDEyMzRkIn0sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9

blows up: https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLnBhcnNlZCA9IHBhcnNlX2R1cmF0aW9uISguYmFkLCBcInNcIikiLCJldmVudCI6eyJiYWQiOiIxMjM0NTY3ODkwMTIzNDU2Nzg5MDEyMzQ1ZCJ9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

### Additional Context

_No response_

### References

_No response_
