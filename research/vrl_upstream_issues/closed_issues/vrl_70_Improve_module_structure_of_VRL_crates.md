# Issue #70: Improve module structure of VRL crates

- **URL:** https://github.com/vectordotdev/vrl/issues/70
- **Author:** @JeanMertz
- **Status:** CLOSED (completed)
- **Created:** 2022-04-22T05:55:50Z
- **Closed:** 2023-06-21T13:40:51Z
- **Labels:** vrl:compiler, type:tech debt

## Description

VRL's module structure has grown organically, and has become more unclear as time passed. Especially when implementing stdlib functions, and having to write non-standard tests (in my case, when wanting to write a test that validates closure behaviour), numerous modules have to pulled in from different places, sometimes through `vrl::prelude`, which makes it unclear what is going on.

I'm not proposing removing `prelude` (it's valuable to stdlib authors that aren't as familiar with Rust), but we should trim it, focus it, and also audit all other modules in VRL crates.
