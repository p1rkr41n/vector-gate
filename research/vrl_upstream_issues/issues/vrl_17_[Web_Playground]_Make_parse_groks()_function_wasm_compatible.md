# [#17] [Web Playground] Make parse_groks() function wasm compatible

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/17)
- **Status**: `OPEN`
- **Author**: [@jonathanpv](https://github.com/jonathanpv)
- **Created At**: `2022-10-03T21:16:32Z`
- **Updated At**: `2026-06-16T13:10:35Z`
- **Comments**: 2
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:parse_groks`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/17)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

```shell
jon.padilla@COMP-W936N7C769 wasm % wasm-pack build --target web && python3 -m http.server
[INFO]: 🎯  Checking for the Wasm target...
[INFO]: 🌀  Compiling to Wasm...
   Compiling cc v1.0.73
   Compiling pkg-config v0.3.25
   Compiling glob v0.3.0
   Compiling bitflags v1.3.2
   Compiling peeking_take_while v1.0.0
   Compiling datadog-grok v0.1.0 (/Users/jon.padilla/Documents/datadoge/vector/lib/datadog/grok)
   Compiling value v0.1.0 (/Users/jon.padilla/Documents/datadoge/vector/lib/value)
   Compiling grok v2.0.0
   Compiling onig_sys v69.8.1
   Compiling vector-common v0.1.0 (/Users/jon.padilla/Documents/datadoge/vector/lib/vector-common)
   Compiling vrl-core v0.1.0 (/Users/jon.padilla/Documents/datadoge/vector/lib/vrl/core)
The following warnings were emitted during compilation:

warning: In file included from oniguruma/src/regexec.c:36:
warning: oniguruma/src/regint.h:110:10: fatal error: 'stdlib.h' file not found
warning: #include <stdlib.h>
warning:          ^~~~~~~~~~
warning: 1 error generated.

error: failed to run custom build command for `onig_sys v69.8.1`

Caused by:
  process didn't exit successfully: `/Users/jon.padilla/Documents/datadoge/vector/target/release/build/onig_sys-ecd020a4d90c735e/build-script-build` (exit status: 1)
  --- stdout
  cargo:rerun-if-env-changed=RUSTONIG_DYNAMIC_LIBONIG
  cargo:rerun-if-env-changed=RUSTONIG_STATIC_LIBONIG
  cargo:rerun-if-env-changed=RUSTONIG_SYSTEM_LIBONIG
  TARGET = Some("wasm32-unknown-unknown")
  OPT_LEVEL = Some("3")
  HOST = Some("aarch64-apple-darwin")
  CC_wasm32-unknown-unknown = None
  CC_wasm32_unknown_unknown = None
  TARGET_CC = None
  CC = None
  CFLAGS_wasm32-unknown-unknown = None
  CFLAGS_wasm32_unknown_unknown = None
  TARGET_CFLAGS = None
  CFLAGS = None
  CRATE_CC_NO_DEFAULTS = None
  DEBUG = Some("false")
  running: "clang" "-O3" "-ffunction-sections" "-fdata-sections" "-fPIC" "--target=wasm32-unknown-unknown" "-I" "/Users/jon.padilla/Documents/datadoge/vector/target/wasm32-unknown-unknown/release/build/onig_sys-e919ee5bf7cf8573/out" "-I" "oniguruma/src" "-DONIG_DISABLE_DIRECT_THREADING=1" "-DONIG_EXTERN=__attribute__((visibility(\"default\")))" "-o" "/Users/jon.padilla/Documents/datadoge/vector/target/wasm32-unknown-unknown/release/build/onig_sys-e919ee5bf7cf8573/out/oniguruma/src/regexec.o" "-c" "oniguruma/src/regexec.c"
  cargo:warning=In file included from oniguruma/src/regexec.c:36:
  cargo:warning=oniguruma/src/regint.h:110:10: fatal error: 'stdlib.h' file not found
  cargo:warning=#include <stdlib.h>
  cargo:warning=         ^~~~~~~~~~
  cargo:warning=1 error generated.
  exit status: 1

  --- stderr


  error occurred: Command "clang" "-O3" "-ffunction-sections" "-fdata-sections" "-fPIC" "--target=wasm32-unknown-unknown" "-I" "/Users/jon.padilla/Documents/datadoge/vector/target/wasm32-unknown-unknown/release/build/onig_sys-e919ee5bf7cf8573/out" "-I" "oniguruma/src" "-DONIG_DISABLE_DIRECT_THREADING=1" "-DONIG_EXTERN=__attribute__((visibility(\"default\")))" "-o" "/Users/jon.padilla/Documents/datadoge/vector/target/wasm32-unknown-unknown/release/build/onig_sys-e919ee5bf7cf8573/out/oniguruma/src/regexec.o" "-c" "oniguruma/src/regexec.c" with args "clang" did not execute successfully (status code exit status: 1).


warning: build failed, waiting for other jobs to finish...
Error: Compiling your crate to WebAssembly failed
Caused by: failed to execute `cargo build`: exited with exit status: 101
  full command: "cargo" "build" "--lib" "--release" "--target" "wasm32-unknown-unknown"
jon.padilla@COMP-W936N7C769 wasm %    
```

ref: vectordotdev/vector#14654
ref: vectordotdev/vrl#22
