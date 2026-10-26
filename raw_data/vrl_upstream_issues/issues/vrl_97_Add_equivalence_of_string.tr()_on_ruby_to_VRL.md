# [#97] Add equivalence of string.tr() on ruby to VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/97)
- **Status**: `OPEN`
- **Author**: [@Steuf](https://github.com/Steuf)
- **Created At**: `2021-08-18T14:47:35Z`
- **Updated At**: `2023-03-28T13:55:23Z`
- **Comments**: 4
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/97)

---

## Description

### Current Vector Version 

```
0.15.2
```

### Use-cases

Using a custom base64 encoding on log, before use of base64decode we need to replace some chars on string to re-transform it on a valid base64 string.

### Attempted Solutions

Can be done today with usage of LUA transform with the function string.gsub.

### Proposal

Add a new function equivalent of string.tr() on ruby on VRL to avoid usage of lua script.

### References

https://apidock.com/ruby/String/tr

