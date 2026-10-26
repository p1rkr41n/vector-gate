# [#141] rename `to_syslog_severity` to `parse_syslog_severity`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/141)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2021-01-09T20:55:44Z`
- **Updated At**: `2026-06-16T13:11:46Z`
- **Comments**: 3
- **Labels**: `vrl:stdlib`, `stdlib:to_syslog_severity`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/141)

---

## Description

This one is incorrectly named. It behaves similar to other `parse_*` functions (take in a string, try to parse it to the relevant type, error if it can't), but is named as a `to_*` function.
