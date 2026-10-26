# Issue #367: once_cell support by move from anymap to anymap2

- **URL:** https://github.com/vectordotdev/vrl/issues/367
- **Author:** @avmartugin
- **Status:** CLOSED (not_planned)
- **Created:** 2023-08-03T06:38:42Z
- **Closed:** 2023-09-28T01:43:14Z
- **Labels:** None

## Description

now impossible to use once_cell because Sync or Send does not implemented for AnyMap in anymap crate, but anymap2 does.
need to move for reduce compile overhead each time if use same vrl programm
