# [#21] Expand VRL test harness to allow running tests in WASM environment

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/21)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-09-30T12:35:56Z`
- **Updated At**: `2023-03-28T13:09:55Z`
- **Comments**: 5
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/21)

---

## Description

While working on vectordotdev/vector#14653 and vectordotdev/vector#14654 we need a way to ensure that the gains achieved in those tasks aren't lost over time. To ensure Wasm compilation (and runtime) continues to function, we should expand our [test harness](https://github.com/vectordotdev/vector/tree/bf6efe98887ce65f58ef06e2b26159d452fb01a4/lib/vrl/tests) to allow running the tests in the `wasm32-unknown-unknown` environment.

This allows us to catch potential issues through our continuous integration set-up, providing a robust level of guarantee that the playground continues to function for users as development moves forward.
