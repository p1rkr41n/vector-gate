# [#777] Parse/Encode logfmt is not idempotent when values have double quotes

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/777)
- **Status**: `OPEN`
- **Author**: [@srstrickland](https://github.com/srstrickland)
- **Created At**: `2024-03-30T01:57:46Z`
- **Updated At**: `2026-06-01T14:07:33Z`
- **Comments**: 7
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/777)

---

## Description

In general, any encode/decode function pairs should be idempotent; that is, this should always be true:

```
x == decode(encode(x))
```

It appears to not be the case with `encode_logfmt` and `parse_logfmt`, as [demonstrated here](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLm9iai5rZXkgPSBzJ3RoaXMgaGFzIGEgXCIgcXVvdGUnXG4ucmVzdWx0ID0gcGFyc2VfbG9nZm10IShlbmNvZGVfbG9nZm10KC5vYmopKSIsImV2ZW50Ijp7fSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D), where `result.key` has additional escape characters.

Taken to the extreme:

```
.obj.key = s'this has a " quote'
parse_logfmt!(encode_logfmt(parse_logfmt!(encode_logfmt(parse_logfmt!(encode_logfmt(parse_logfmt!(encode_logfmt(parse_logfmt!(encode_logfmt(.obj))))))))))
```

yields:

```
{ "key": "this has a \\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\\" quote" }
```

This isn't really causing me any headaches, and the fact that it hasn't been raised yet probably indicates the same for other folks, just thought it was worth bringing up, as I stumbled on it today.
