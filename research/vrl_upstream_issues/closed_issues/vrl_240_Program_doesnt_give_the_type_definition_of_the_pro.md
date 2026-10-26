# Issue #240: `Program` doesn't give the type definition of the program result

- **URL:** https://github.com/vectordotdev/vrl/issues/240
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2023-05-13T01:21:30Z
- **Closed:** 2023-05-31T18:26:42Z
- **Labels:** type:enhancement, vrl:typedef

## Description

Currently the `Program` type (returned from compiling a VRL program) gives you access to the type definitions of the target and locals through the `Program::final_type_state` function. There is no type definition for the result itself (the `Value` returned from `resolve`).
