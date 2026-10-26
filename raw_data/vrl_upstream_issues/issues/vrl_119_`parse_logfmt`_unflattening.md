# [#119] `parse_logfmt` unflattening

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/119)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2021-05-04T17:20:33Z`
- **Updated At**: `2026-06-16T13:11:32Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:parse_logfmt`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/119)

---

## Description

When encoding as `logfmt`, it is common to flatten structured data. For example:

```json
{
  "foo": {
    "bar": 1
  }
}
```

Would be encoded as `foo.bar=1` in logfmt.

Currently, the parser just reads the keys as-is so you end up with an object like:

```json
{
  "foo.bar": 1
}
```

I think it'd be nice to unflatten. This could be an optional behavior.

Notably the PR adding `encode_logfmt` (https://github.com/timberio/vector/pull/6985) does this flattening.


