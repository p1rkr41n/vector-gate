# Issue #124: Add `to_entries` and `from_entries` to VRL

- **URL:** https://github.com/vectordotdev/vrl/issues/124
- **Author:** @jszwedko
- **Status:** CLOSED (completed)
- **Created:** 2021-04-16T19:50:57Z
- **Closed:** 2026-04-03T19:07:25Z
- **Labels:** type:enhancement, vrl:stdlib

## Description

Inspired by user in discord: https://discord.com/channels/742820443487993987/746070591097798688/832684085771370587

The user would like to transform:

```json
{
  "labels": {
    "key1": "value1",
    "key2": "value2"
  }
}
```

into

```json
{
  "labels": [
    {
      "key": "key1",
      "value": "value1"
    },
    {
      "key": "key2",
      "value": "value2"
    }
  ]
}
```

I think `jq`'s `to_entries` and `from_entries` are good approaches to this.
