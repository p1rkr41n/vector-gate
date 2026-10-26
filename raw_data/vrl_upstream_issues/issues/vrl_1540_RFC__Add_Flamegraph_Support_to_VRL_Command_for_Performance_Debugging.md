# [#1540] RFC: Add Flamegraph Support to VRL Command for Performance Debugging

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1540)
- **Status**: `OPEN`
- **Author**: [@jlambatl](https://github.com/jlambatl)
- **Created At**: `2025-10-15T23:16:08Z`
- **Updated At**: `2026-06-01T14:19:40Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1540)

---

## Description

### A note for the community

Add flamegraph profiling capabilities to the `vector vrl` command to help users identify performance bottlenecks in their VRL (Vector Remap Language) scripts. This feature would generate interactive flame graphs showing function call hierarchies and execution time distribution, making it easier to optimise VRL transformations.

## Motivation

VRL scripts can become complex and performance-critical in production Vector deployments. Currently, users have limited visibility into VRL performance characteristics and must rely on:

- Manual timing with `print` statements
- High-level metrics from Vector's observability
- Trial-and-error optimisation approaches


<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritise this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

This proposal addresses the need for detailed, function-level performance profiling to help users:

1. Identify hot paths in complex VRL scripts
2. Optimise expensive operations like regex matching, parsing, or nested object manipulation
3. Debug unexpected performance degradation when modifying existing scripts
4. Validate performance improvements after optimisation attempts

### Attempted Solutions

While flamegraphs are one solution, we could opt for a standardised output format and allow teams to use tools that they prefer, one such example could be pprof, although I am open to suggestion.

### Proposal

### New CLI Options

Add profiling flags to the existing `vector vrl` command:

```bash
# Generate flamegraph for a VRL script
vector vrl --flamegraph <output> -p script.vrl -i input.json
```

This could also be
```bash
# Generate profiling output for a VRL script
vector vrl --profiler <output> -p script.vrl -i input.json
```



### References

_No response_
