# Issue #1163: Move core VRL documentation out of Vector

- **URL:** https://github.com/vectordotdev/vrl/issues/1163
- **Author:** @bruceg
- **Status:** CLOSED (completed)
- **Created:** 2024-12-03T18:37:37Z
- **Closed:** 2024-12-03T18:40:24Z
- **Labels:** type:tech debt, domain:dev, domain:ci

## Description

All of the documentation describing VRL actually lives in the Vector repository as part of the [remap reference manual](https://github.com/vectordotdev/vector/tree/master/website/cue/reference/remap). This results in the complication where a change to VRL requires changing both repositories in order to keep the documentation aligned.

It would be helpful for development experience to move the documentation for VRL into this repository such that changes to the core of VRL do not require corresponding changes to Vector other than pulling in the new revision dependency. This will, of course, require building up at least a little infrastructure here to check and possibly format the docs during building and/or CI.
