# [#471] parse_klog always parse the timestamp as UTC timezone

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/471)
- **Status**: `OPEN`
- **Author**: [@Leo1003](https://github.com/Leo1003)
- **Created At**: `2023-09-23T23:38:27Z`
- **Updated At**: `2026-06-16T13:10:20Z`
- **Comments**: 3
- **Labels**: `stdlib:parse_klog`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/471)

---

## Description

The logs outputs from kubelet are emitted with local timezone timestamp, however, the `parse_klog()` (and maybe also `parse_glog()`) function always parses them as UTC timestamp. This leads to hours of time shifting in the parsed log.
