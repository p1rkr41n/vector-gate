# [#132] Add summary of passed/skipped/failed tests to VRL test harness

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/132)
- **Status**: `OPEN`
- **Author**: [@bruceg](https://github.com/bruceg)
- **Created At**: `2021-03-12T16:46:20Z`
- **Updated At**: `2023-03-28T14:28:51Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `domain:tests`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/132)

---

## Description

When running `cargo test`, cargo will print a summary of the numbers of tests run, as well as a listing of which ones failed. The VRL test suite has grown large enough to make scrolling through the listing to see which one(s) failed tedious. This could be improved by providing a similar summary of the test run after completion.

Ref: https://github.com/timberio/vector/pull/6738/checks?check_run_id=2096688778
