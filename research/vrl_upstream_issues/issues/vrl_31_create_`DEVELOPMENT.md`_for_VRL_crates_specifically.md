# [#31] create `DEVELOPMENT.md` for VRL crates specifically

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/31)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-08-23T20:13:46Z`
- **Updated At**: `2023-03-28T13:17:31Z`
- **Comments**: 1
- **Labels**: `domain:dev`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/31)

---

## Description

Reading through this blog post:

https://briankung.dev/2022/08/18/contributing-to-the-vector-remap-language/

It reads:

> From a language ergonomics perspective, while I still enjoyed using Rust, the compile times did become painful. Compiling a debug version of vector from scratch took 7 minutes and 30 seconds. I later switched to using the mold linker and it went down to 6 minutes, but it was still disruptive. Meanwhile, a full release mode compile would take 14 minutes on my Core i9 iMac. Thankfully, incremental compiles were much quicker.

It would have likely saved several minutes of compilation time if the contributor had known that you can compile _only_ the `stdlib` crate, and within that crate _only_ the specific function(s) you're working with.

It's probably worth documenting this in a dedicated `DEVELOPMENT.md` file under `lib/vrl`.
