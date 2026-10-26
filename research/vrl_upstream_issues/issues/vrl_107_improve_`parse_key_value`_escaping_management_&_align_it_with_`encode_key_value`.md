# [#107] improve `parse_key_value` escaping management & align it with `encode_key_value`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/107)
- **Status**: `OPEN`
- **Author**: [@prognant](https://github.com/prognant)
- **Created At**: `2021-07-01T14:35:52Z`
- **Updated At**: `2026-06-16T13:11:28Z`
- **Comments**: 4
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:parse_key_value`, `stdlib:encode_key_value`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/107)

---

## Description

`parse_key_value` has limited escaping support for some sequence, however the parsing does not remove the escaping character, this is inconsistent with `encode_key_value` that adds escape character causing  `parse_key_value(encode_key_value(...))` not to be a noop (I'm not sure it is even if there is no escaped character, it should but that's not the point here).

```
$ parse_key_value!(s'foo="\"bar\""', whitespace:"strict")
{ "foo": "\\\"bar\\\"" }
```
whereas it should be

```
{ "foo": "\"bar\"" }
```

Test cases that would have to be updated (as of today they are not in master)
https://github.com/timberio/vector/blob/2ce9ddfdb53792e24e3d0360a713f490f717ebb7/lib/vrl/stdlib/src/parse_key_value.rs#L557-L573
