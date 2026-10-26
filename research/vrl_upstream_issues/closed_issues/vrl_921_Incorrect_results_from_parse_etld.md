# Issue #921: Incorrect results from parse_etld

- **URL:** https://github.com/vectordotdev/vrl/issues/921
- **Author:** @DylanRJohnston
- **Status:** CLOSED (completed)
- **Created:** 2024-07-03T02:40:37Z
- **Closed:** 2024-07-03T03:02:21Z
- **Labels:** None

## Description

When invoking `parse_etld` for the domain `test.servicebus.windows.net` VRL gives the following results

[Playground Link](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLiA9IHBhcnNlX2V0bGQhKFwidGVzdC5zZXJ2aWNlYnVzLndpbmRvd3MubmV0XCIsIDEpIiwiZXZlbnQiOnt9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D)
```json
{
  "etld":"servicebus.windows.net",
  "etld_plus":"test.servicebus.windows.net",
  "known_suffix":true
}
```

When the correct response is

```json
{
  "etld":"net",
  "etld_plus":"windows.net",
  "known_suffix":true
}
```

It seems to incorrectly identify the eTLD as `servicebus.windows.net` instead of `net`. 


