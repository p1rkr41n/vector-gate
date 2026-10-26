# [#104] `unnest` should unnest one level deeper

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/104)
- **Status**: `OPEN`
- **Author**: [@StephenWakely](https://github.com/StephenWakely)
- **Created At**: `2021-07-13T23:15:38Z`
- **Updated At**: `2026-06-16T13:11:26Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:unnest`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/104)

---

## Description

As noted on [discord](https://discord.com/channels/742820443487993987/759154784309215252/864642159377383445).

Say you have an event of:

```json
{ "things": [{ "id": 1, "thing": "thong" }, { "id": 2, "thang": "thung" }], "timestamp": "monday" }
```

and you run:
```
. = unnest(.things)
```

This gives you an event array of:

```json
[{ "things": { "id": 1, "thing": "thong" }, "timestamp": "monday" }, 
 { "things": { "id": 2, "thang": "thung" }, "timestamp": "monday" }]
```

It seems much more likely that the user is going to want the result to be:

```json
[{ "id": 1, "thing": "thong", "timestamp": "monday" }, 
 { "id": 2, "thang": "thung", "timestamp": "monday" }]
```

We should either just change unnest to work this way, or perhaps make it parameterised so the user has an option as to which way it should work.

