# [#96] Add function is_uuid on VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/96)
- **Status**: `OPEN`
- **Author**: [@Steuf](https://github.com/Steuf)
- **Created At**: `2021-08-18T16:37:56Z`
- **Updated At**: `2023-03-28T13:55:04Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/96)

---

## Description

### Current Vector Version

```
0.15.2
```

### Use-cases

Check if the value of field are a valid uuid

### Attempted Solutions

Can be done by a regex match :

```
        if exists(.uuid) && !match(.uuid, r'^[0-9a-fA-F]{8}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{4}\-[0-9a-fA-F]{12}$') {
          .uuid = "00000000-0000-0000-0000-000000000000"
        }
```

### Proposal

Add a native function is_uuid to check if the string is a valid uuid, I think I will be more performant than a regex ;)

### References

https://docs.rs/rubble/0.0.3/rubble/uuid/trait.IsUuid.html

