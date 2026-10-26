# [#143] Add Remap function for comparing semantic versions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/143)
- **Status**: `OPEN`
- **Author**: [@lucperkins](https://github.com/lucperkins)
- **Created At**: `2020-12-15T15:59:45Z`
- **Updated At**: `2023-03-28T14:36:01Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/143)

---

## Description

I'm not sure I can think of an absolute must-have use case, but we should enable users to compare versions of things, like so:

```
semver::compare(v1, v2)
```

This idea is inspired by [Rego](https://www.openpolicyagent.org/docs/latest/policy-language)'s [`semver.compare`](https://www.openpolicyagent.org/docs/latest/policy-reference/#semantic-versions) function, which returns three possible integers:

* 1 if v1 is later than v2
* 0 if the two versions are the same
* -1 if v1 is earler than v2

This would allow for constructing Boolean expressions:

```
if (semver::compare(.version, "1.0") == -1) {
    .deprecated = true
}
```

I'm open to other interfaces for this, for example:

```
semver::compare(v1, v2, expect = ["gt"]) // Boolean

semver::parse(v1) > semver::parse(v2)
```
