# [#133] It is possible to create excessively huge arrays in VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/133)
- **Status**: `OPEN`
- **Author**: [@StephenWakely](https://github.com/StephenWakely)
- **Created At**: `2021-03-03T09:46:54Z`
- **Updated At**: `2023-03-28T14:29:25Z`
- **Comments**: 4
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/133)

---

## Description

In VRL running:

```
.thing[9223372036854775807] = 1
```

will cause VRL to attempt to allocate a huge array. This basically locks it up and will likely crash it eventually (I didn't wait long enough to find out for sure).

We should probably put a reasonable limit in here to prevent this from occurring.

This will become much more important when we allow variables to be used as array indexers.
