# [#82] chore(vrl): explore arena allocation for VRL programs

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/82)
- **Status**: `OPEN`
- **Author**: [@tobz](https://github.com/tobz)
- **Created At**: `2022-01-25T16:53:37Z`
- **Updated At**: `2023-03-28T13:46:39Z`
- **Comments**: 1
- **Labels**: `type:enhancement`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/82)

---

## Description

As a thought experiment: could we use an arena allocator for VRL programs to authoritatively constrain their runtime memory usage as well as speed up allocations?

Currently, there are some suboptimal allocation patterns that we'd like to remove from VRL execution in general, but when dealing with non-scalar data types (maps, lists, etc), and including externally-imported code (such as codec parsers), we inevitably perform heap allocations.

This introduces unwelcome allocator pressure, and potentially hard-to-defragment allocations, which typically don't need to live past the execution of the program, as we frequently clone the value on the way out of VRL.

It could potentially be advantageous to use an arena allocator for all heap allocations in a VRL program.  Arena allocators are typically used for scenarios where there is "phase-oriented" allocations, or allocation that happens as part of a logical operation, and then can be totally cleaned up once that operation is over.  VRL program execution, as it is stateless between program runs, fits this model well.

Separate from the potential speedups of phase-oriented allocation/deallocation, it could also be useful to use a dedicated allocator as doing so would allow constraining the memory usage in a very precise manner, as most arena allocators are fixed-sized, or can operate in fixed-size modes.  This would finally allow us to concretely represent how much memory a VRL program could consume, which would be the sum of the thread stack size and the arena allocator size.
