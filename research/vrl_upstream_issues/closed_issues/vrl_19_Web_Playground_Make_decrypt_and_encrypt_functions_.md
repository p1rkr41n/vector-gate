# Issue #19: [Web Playground] Make `decrypt()` and `encrypt()` functions wasm compatible

- **URL:** https://github.com/vectordotdev/vrl/issues/19
- **Author:** @jonathanpv
- **Status:** CLOSED (completed)
- **Created:** 2022-10-03T21:12:28Z
- **Closed:** 2023-04-01T00:24:10Z
- **Labels:** type:enhancement, vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Currently the decrypt and encrypt functions have these errors when attempting to compile to wasm. 
```shell
jon.padilla@COMP-W936N7C769 wasm % wasm-pack build --target web && python3 -m http.server
[INFO]: 🎯  Checking for the Wasm target...
[INFO]: 🌀  Compiling to Wasm...
   Compiling ppv-lite86 v0.2.16
   Compiling getrandom v0.2.6
   Compiling block-padding v0.3.2
error: the wasm32-unknown-unknown target is not supported by default, you may need to enable the "js" feature. For more information see: https://docs.rs/getrandom/#webassembly-support
   --> /Users/jon.padilla/.cargo/registry/src/github.com-1ecc6299db9ec823/getrandom-0.2.6/src/lib.rs:235:9
    |
235 | /         compile_error!("the wasm32-unknown-unknown target is not supported by \
236 | |                         default, you may need to enable the \"js\" feature. \
237 | |                         For more information see: \
238 | |                         https://docs.rs/getrandom/#webassembly-support");
    | |________________________________________________________________________^

error[E0433]: failed to resolve: use of undeclared crate or module `imp`
   --> /Users/jon.padilla/.cargo/registry/src/github.com-1ecc6299db9ec823/getrandom-0.2.6/src/lib.rs:262:5
    |
262 |     imp::getrandom_inner(dest)
    |     ^^^ use of undeclared crate or module `imp`

For more information about this error, try `rustc --explain E0433`.
error: could not compile `getrandom` due to 2 previous errors
warning: build failed, waiting for other jobs to finish...
Error: Compiling your crate to WebAssembly failed
Caused by: failed to execute `cargo build`: exited with exit status: 101
  full command: "cargo" "build" "--lib" "--release" "--target" "wasm32-unknown-unknown"
jon.padilla@COMP-W936N7C769 wasm % 
```

ref: vectordotdev/vector#14654
ref: vectordotdev/vrl#22
