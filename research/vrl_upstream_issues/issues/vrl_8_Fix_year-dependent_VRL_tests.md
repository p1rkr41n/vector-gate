# [#8] Fix year-dependent VRL tests

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/8)
- **Status**: `OPEN`
- **Author**: [@bruceg](https://github.com/bruceg)
- **Created At**: `2023-01-04T17:07:46Z`
- **Updated At**: `2025-01-02T18:46:35Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`, `type:tech debt`, `domain:tests`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/8)

---

## Description

With vectordotdev/vector#15797 we applied a bandaid to the two year-dependent VRL tests, `parse_klog` and `parse_linux_authorization`, but they will again fail next year if nothing is changed. This needs to be resolved so we don't continue to have yearly issues with these tests.
