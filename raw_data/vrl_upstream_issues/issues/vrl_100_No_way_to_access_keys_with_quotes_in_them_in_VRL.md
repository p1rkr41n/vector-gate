# [#100] No way to access keys with quotes in them in VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/100)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2021-08-04T14:38:19Z`
- **Updated At**: `2026-06-01T14:04:54Z`
- **Comments**: 0
- **Labels**: `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/100)

---

## Description

There doesn't _appear_ to be a way to access keys that literally have `"`s in them in VRL.

```
vector 0.15.0 (x86_64-apple-darwin 994d812 2021-07-16)
```

```
$ . = { "event": {"\"log\"": 1 }}
$ .event
{ ""log"": 1 }
$ .event."\"log\""
null
```
