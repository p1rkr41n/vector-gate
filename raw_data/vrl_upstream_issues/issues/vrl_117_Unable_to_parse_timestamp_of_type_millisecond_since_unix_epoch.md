# [#117] Unable to parse timestamp of type millisecond since unix epoch

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/117)
- **Status**: `OPEN`
- **Author**: [@jerome-kleinen-kbc-be](https://github.com/jerome-kleinen-kbc-be)
- **Created At**: `2021-05-06T11:07:48Z`
- **Updated At**: `2026-06-01T14:04:42Z`
- **Comments**: 6
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/117)

---

## Description

<!--
Hi there,

Thank you for opening an issue. Please note that we try to keep the Vector issue tracker reserved for bug reports and feature requests. For general usage questions, please see: https://chat.vector.dev.
-->

### Vector Version

<!---
Run `vector --version` to show the version, and paste the result between the ``` marks below.

If you are not running the latest version of Vector, please try upgrading because your issue may have already been fixed.
-->

```
vector 0.13.1 (v0.13.1 x86_64-unknown-linux-gnu 2021-04-29)
```

### Vector Configuration File

```
$ parse_timestamp!("1620291751177", "%s%3f")
function call error for "parse_timestamp" at (0:42): Invalid timestamp "1620291751177": premature end of input

$ parse_timestamp!("1620291751.177", "%s%.3f")
t'2021-05-06T09:02:31.177Z'
```

### Debug Output

N/A


### Expected Behavior

The first parse_timestamp command should have been able to parse the timestamp.

### Actual Behavior

It didn't parse the timestamp.


