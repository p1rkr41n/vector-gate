# Issue #1120: `to_float` and `parse_float` should have the same implementation

- **URL:** https://github.com/vectordotdev/vrl/issues/1120
- **Author:** @pront
- **Status:** CLOSED (completed)
- **Created:** 2024-11-11T16:40:08Z
- **Closed:** 2024-12-09T20:48:15Z
- **Labels:** type:tech debt

## Description

While working on https://github.com/vectordotdev/vrl/issues/1107, I realized that `parse_float` doesn't share the same implementation as `to_float`. The latter has a more generic implementation that can replace the former. Same for `to_int` and `parse_int`.

Since 0.43 these deviated, see [playground example](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLmEsIC5lcnIxID0gdG9fZmxvYXQoXCIrMFwiKVxuLmIsIC5lcnIyID0gdG9fZmxvYXQoXCItMFwiKSBcblxuLmMsIC5lcnIzID0gcGFyc2VfZmxvYXQoXCIrMFwiKVxuLmQsIC5lcnI0ID0gcGFyc2VfZmxvYXQoXCItMFwiKSBcbi5lLCAuZXJyNSA9IHBhcnNlX2Zsb2F0KFwiMFwiKSBcbiIsImV2ZW50Ijp7fSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D) (needs VRL version v.20.0).
