# [#18] [Web Playground] Make get_hostname() function wasm compatible 

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/18)
- **Status**: `OPEN`
- **Author**: [@jonathanpv](https://github.com/jonathanpv)
- **Created At**: `2022-10-03T21:14:33Z`
- **Updated At**: `2026-06-16T13:10:38Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:get_hostname`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/18)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Current error message when attempting to compile to wasm

```shell
jon.padilla@COMP-W936N7C769 wasm % wasm-pack build --target web && python3 -m http.server
[INFO]: 🎯  Checking for the Wasm target...
[INFO]: 🌀  Compiling to Wasm...
   Compiling match_cfg v0.1.0
   Compiling hostname v0.3.1
error: Unsupported target OS! Create an issue: https://github.com/svartalf/hostname/issues/new
  --> /Users/jon.padilla/.cargo/registry/src/github.com-1ecc6299db9ec823/hostname-0.3.1/src/lib.rs:81:9
   |
81 |         compile_error!("Unsupported target OS! Create an issue: https://github.com/svartalf/hostname/issues/new");
   |         ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

error[E0433]: failed to resolve: use of undeclared crate or module `sys`
   --> /Users/jon.padilla/.cargo/registry/src/github.com-1ecc6299db9ec823/hostname-0.3.1/src/lib.rs:105:5
    |
105 |     sys::get()
    |     ^^^ use of undeclared crate or module `sys`

For more information about this error, try `rustc --explain E0433`.
error: could not compile `hostname` due to 2 previous errors
Error: Compiling your crate to WebAssembly failed
Caused by: failed to execute `cargo build`: exited with exit status: 101
  full command: "cargo" "build" "--lib" "--release" "--target" "wasm32-unknown-unknown"
jon.padilla@COMP-W936N7C769 wasm % 
```

ref: vectordotdev/vector#14654
ref: vectordotdev/vrl#22
