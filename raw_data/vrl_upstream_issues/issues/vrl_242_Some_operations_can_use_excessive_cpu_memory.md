# [#242] Some operations can use excessive cpu/memory

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/242)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2023-05-13T01:41:25Z`
- **Updated At**: `2026-06-01T14:06:50Z`
- **Comments**: 1
- **Labels**: `vrl:compiler`, `fuzz`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/242)

---

## Description

Assigning a value to a very large (positive or negative) index will expand the array to the size required to fit that index, potentially using an excessive amount of memory. A large limit (e.g. 1 million?) that causes an abort may help prevent abuse or accidents here.

Examples
```coffee
x[99999999999] = true;
```
```coffee
x[-99999999999] = true;
```

List of known areas that can excessively allocate:
- assigning to large array indices
- multiplying a string (bytes) by a large number
