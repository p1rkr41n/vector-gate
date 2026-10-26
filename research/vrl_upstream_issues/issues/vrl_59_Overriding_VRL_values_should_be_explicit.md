# [#59] Overriding VRL values should be explicit

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/59)
- **Status**: `OPEN`
- **Author**: [@binarylogic](https://github.com/binarylogic)
- **Created At**: `2022-06-01T16:47:13Z`
- **Updated At**: `2023-03-28T13:32:05Z`
- **Comments**: 3
- **Labels**: `type:enhancement`, `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/59)

---

## Description

This issue falls out of the foot gun demonstrated in https://github.com/vectordotdev/vector/pull/12929. It is somewhat related to vectordotdev/vector#12701.

Accidentally overriding data in VRL should be disallowed. A principle of VRL is to be safe and this is unsafe. Instead, users should be required explicitly erase data before overriding it:

```
del(.attribute)
.attribute = {...}
```

Or, use an operator that achieves the same thing:

```
.attribute != {...}
```

Open to other operators. Without this, the user would get a compilation error directing them to explicitly override the data using `del` or the special operator.
