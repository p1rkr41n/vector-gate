# [#128] Allow defaulting a non-existent path in VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/128)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2021-04-08T20:33:18Z`
- **Updated At**: `2023-03-28T14:26:12Z`
- **Comments**: 4
- **Labels**: `type:enhancement`, `vrl:compiler`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/128)

---

## Description

Requested by user in discord: https://discord.com/channels/742820443487993987/746070591097798688/829788575234523156

They'd like to be able to lookup a field but set a default if it does not exist. 

This is doable via:

```
$ bar = if exists(.foo) { .foo } else { "not set" }
"not set"
```

But it would be nice to add some sort of null coalescing support similar to the error coalescing we currently have using `??`.
