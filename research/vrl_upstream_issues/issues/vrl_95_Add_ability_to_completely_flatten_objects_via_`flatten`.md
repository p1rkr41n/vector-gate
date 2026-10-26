# [#95] Add ability to completely flatten objects via `flatten`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/95)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2021-08-25T19:40:45Z`
- **Updated At**: `2026-06-16T13:11:20Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:flatten`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/95)

---

## Description

A [user in discord](https://discord.com/channels/742820443487993987/746070591097798688/880125594807971840) was depending on the previous behavior of the `loki` sink to flatten objects like:

```json
{
  "foo": [{"bar": "baz"}]
}
```

To

```json
{
  "foo[0].bar": "baz"
}
```

This behavior was changed in vectordotdev/vector#8044 to send the nested JSON as-is to Loki.

VRL does have a `flatten` function, which I think could support the user's use-case, but this function does not flatten nested arrays and arrays of objects. I think we could extend it to do so; perhaps via an additional parameter.
