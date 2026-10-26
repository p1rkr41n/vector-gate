# [#9] Make VRL WebAssembly artifact production-ready

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/9)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-12-08T15:38:05Z`
- **Updated At**: `2026-01-26T21:10:33Z`
- **Comments**: 3
- **Labels**: `Epic`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/9)

---

## Description

We're currently compiling VRL to Wasm (using the `wasm32-unknown-uknown` target) to be able to run the [VRL Playground](https://playground.vrl.dev) on the web without the need for a server-side component.

We want to leverage this Wasm artifact in more use-cases in the future, but before we can do that, additional steps have to be taken. These are listed out below, tracked in separate issues.

**must haves**

- [ ] Compile and host nightly and stable VRL Wasm binary artifacts

   For the VRL Playground, we currently compile VRL to Wasm as part of the [Netlify build process](https://github.com/vectordotdev/vector/blob/550aa8b1f50c7674fe367d02d8d9777ed35d89d7/lib/vrl/web-playground/netlify.toml) to host the playground website. This is insufficient for a more general purpose VRL Wasm artifact. We need to hook into the existing Vector release workflow, to allow this Wasm artifact to be (1) built for every nightly/stable release, and then (2) upload that artifact next to the existing Vector release artifacts, so that they can be downloaded by others. Currently, VRL would have the same release cadence and versioning as Vector, until vectordotdev/vector#3784 (nice to have) is resolved.

- [ ] Create a VRL Wasm binary that is isolated from the VRL Playground

   The existing VRL Wasm binary is built as part of the [`vrl/web-playground`](https://github.com/vectordotdev/vector/tree/550aa8b1f50c7674fe367d02d8d9777ed35d89d7/lib/vrl/web-playground) crate. We should extract this into a separate `vrl/web` crate, which is separated from any playground-specific code, and provides a generic interface to interact (e.g. compile VRL programs, inspect compilation errors, and run programs against individual targets). Most of this will be copy/paste work, but there's some fine-tuning required. Nothing too involved, though.

- [ ] https://github.com/vectordotdev/vrl/issues/21

   To ensure we don't have any regressions of our Wasm binary, we should run our test harness in both the regular (Unix-based) test environment, and in a Wasm-based environment. These tests should run on our CI, similarly to our existing tests. Note that this is not about adding _new_ tests, but running the existing tests using the Wasm VRL runtime.

**nice to haves**

- [ ] Support all VRL functions in the playground or raise an explicit error if non-supported ones are used

- [x] https://github.com/vectordotdev/vector/issues/3784

   VRL is currently embedded within the Vector repository, and piggybacks on the entire CI and release workflow. This has upsides and downsides, the biggest upside is that it's easier to work on both Vector and VRL at the same time, within a single session (e.g. same repo, same editor, single compilation step, etc.), the biggest downside is that VRL has no independent release cadence, and no independent release notes, this makes it difficult for other users of VRL to know when a Vector update is relevant for their non-Vector use-case. By pulling out VRL into a separate project, the project gains independence, which allows it to set its own release cadence, release notes, and CI workflow (which would be much lighter than the existing Vector workflow). It will also help to get a better overview of pending PRs/issues/discussions related to VRL (our existing tagging system helps, but it's not as optimal).

- [x] https://github.com/vectordotdev/vector/issues/11094

   Before we can tackle vectordotdev/vector#3784, we need to solve this issue first, which is about untangling any existing cross-dependencies between Vector and VRL (of which there are some, but not many).

- [ ] Publish VRL crates on crates.io

   By publishing our existing [VRL crates](https://github.com/vectordotdev/vector/tree/550aa8b1f50c7674fe367d02d8d9777ed35d89d7/lib/vrl) on [crates.io](https://crates.io), we make it easier for other projects to integrate VRL. This is not necessary for projects that use our pre-compiled Wasm binary, but it will be for those that want to deviate from the default build parameters (e.g. if they wish to limit or expand the number of [VRL functions](https://vrl.dev/functions/) available in the build, or incorporate other modifications).
