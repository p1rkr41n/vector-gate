# Issue #579: Using comparison operators with timestamps

- **URL:** https://github.com/vectordotdev/vrl/issues/579
- **Author:** @maksimtor
- **Status:** CLOSED (completed)
- **Created:** 2023-11-27T11:34:24Z
- **Closed:** 2023-11-28T19:36:10Z
- **Labels:** type:enhancement

## Description

Currently there is no support for comparison operators for timestamps. 

```
ts1 = t'2024-04-04T22:22:22.234142Z'
ts2 = t'2024-04-04T22:22:22.234142Z'

res, err = ts1 < ts2

err
```
-> "can't compare timestamp >= timestamp"
