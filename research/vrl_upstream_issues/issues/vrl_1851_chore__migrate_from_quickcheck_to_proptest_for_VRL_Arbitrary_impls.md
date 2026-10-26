# [#1851] chore: migrate from quickcheck to proptest for VRL Arbitrary impls

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1851)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2026-07-08T13:49:16Z`
- **Updated At**: `2026-07-10T17:37:27Z`
- **Comments**: 0
- **Labels**: `type:tech debt`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1851)

---

## Description

## Summary

VRL pulls in both `quickcheck` and `proptest` for property-based testing,
which causes two versions of `rand` in the dependency tree. This issue
tracks the VRL side of consolidating on `proptest`.

Related Vector issue: vectordotdev/vector#25726

## Tasks

- Port `quickcheck::Arbitrary` impls for `Value`, `BorrowedSegment`, and
  `KeyString` to proptest strategies
- Rewrite the `QuickCheck` test in `value/value.rs` as a `proptest!` block
- Drop the `quickcheck` dependency
- Rename the `arbitrary` feature flag to `proptest`
