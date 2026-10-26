# [#284] Change how test runner handles deprecations

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/284)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2023-06-28T21:18:35Z`
- **Updated At**: `2023-07-20T15:42:47Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/284)

---

## Description

## Problem
For deprecated VRL functions we emit deprecation warnings (diagnostic) and this is reflected in the output. Currently, the test runner in `lib/tests/src/main.rs` treats the presence of warnings as a test failure. 

We also define some examples for each VRL function. These examples are used to generate test cases. So, when we deprecate the VRL function, all test cases generated from the examples will start failing.

## Proposal
A potential long-term solution (that would also synergize well with #280) is to ignore deprecation warnings and only check the result.
