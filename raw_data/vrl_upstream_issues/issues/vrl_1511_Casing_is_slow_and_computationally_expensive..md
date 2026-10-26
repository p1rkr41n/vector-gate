# [#1511] Casing is slow and computationally expensive.

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1511)
- **Status**: `OPEN`
- **Author**: [@ForkingFrenzy](https://github.com/ForkingFrenzy)
- **Created At**: `2025-09-17T06:27:29Z`
- **Updated At**: `2026-06-01T14:08:38Z`
- **Comments**: 3
- **Labels**: `vrl:stdlib`, `needs:more info`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1511)

---

## Description

### A note for the community

_No response_

### Problem


The casing functions in vrl are a bit slow.


```
. =  map_keys(., recursive: true) -> |key| { snakecase(key) }
```
### The above code is equivalent to the code below using upcase in terms of performance.
Low: 0.1ms, High: 0.4ms
I tested using vector playground site. I understand that this method isn't the most accurate in terms of performance but the point I am trying to make is that it doesn't have to be accurate to realize that the casing functions are unoptimized.

```
. = map_keys(., true) -> |key| { upcase(key) }
. = map_keys(., true) -> |key| { upcase(key) }
. = map_keys(., true) -> |key| { upcase(key) }
. = map_keys(., true) -> |key| { upcase(key) }
. = map_keys(., true) -> |key| { upcase(key) }
. = map_keys(., true) -> |key| { upcase(key) }
. = map_keys(., true) -> |key| { upcase(key) }
. = map_keys(., true) -> |key| { upcase(key) }
. = map_keys(., true) -> |key| { upcase(key) }
. = map_keys(., true) -> |key| { upcase(key) }
```


### VRL Program

```text

```

### VRL and/or Vector Version

a5706e8

### Debug Output

```text

```

### Example

_No response_

### Additional Context

_No response_

### References

_No response_
