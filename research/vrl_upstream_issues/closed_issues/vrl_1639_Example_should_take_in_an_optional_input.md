# Issue #1639: `Example` should take in an optional input

- **URL:** https://github.com/vectordotdev/vrl/issues/1639
- **Author:** @thomasqueirozb
- **Status:** CLOSED (completed)
- **Created:** 2026-02-13T16:38:05Z
- **Closed:** 2026-02-24T22:52:31Z
- **Labels:** None

## Description

In #1564, a bunch of examples were synced from the Vector repo. However, some examples where using an input before and the workaround for this was to add a `. = { "foo": "bar" }` to simulate the input. This is a bit misleading because it gives type information that VRL would usually not have when parsing events coming in from the input.

See the [Valid Boolean from path](https://github.com/vectordotdev/vrl/pull/1564/changes#diff-d9839640b8c46c4dbd7d5b39b0eb36ddb2fc06eb3b6a9fbf22370d27d3b8b1e1) example and the [equivalent example in the Vector repo](https://github.com/vectordotdev/vector/blob/d10f3a5b892833232002c97f24bf008dbef1eeec/website/cue/reference/remap/functions/bool.cue#L28-L37) for a reference.
