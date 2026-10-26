# Issue #238: Multiplication overflows can panic (in debug builds)

- **URL:** https://github.com/vectordotdev/vrl/issues/238
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2023-05-12T18:59:28Z
- **Closed:** 2023-05-24T19:15:32Z
- **Labels:** fuzz

## Description

The following VRL code will panic (when compiled in debug mode). In release mode, it will wrap.

```coffee
444111111111*1111111111111111
```

VRL version: `0.4.0`
