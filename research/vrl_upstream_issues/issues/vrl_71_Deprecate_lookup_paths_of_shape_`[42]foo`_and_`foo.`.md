# [#71] Deprecate lookup paths of shape `[42]foo` and `foo.`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/71)
- **Status**: `OPEN`
- **Author**: [@pablosichert](https://github.com/pablosichert)
- **Created At**: `2022-04-20T20:51:04Z`
- **Updated At**: `2026-06-01T14:05:25Z`
- **Comments**: 0
- **Labels**: `vrl:syntax`, `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/71)

---

## Description

vectordotdev/vector#12306 surfaced that `lookup` currently allows creating paths of shape `[42]foo` and `foo.`.

This behavior should be deprecated, and tests added back to https://github.com/vectordotdev/vector/pull/12306/commits/fb1da4e5ee9d03c7e7e7281de25dd7149f6f518b that assert that these paths are invalid.
