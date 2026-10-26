# [#1960] feat(compiler): support first-class for loops with break and continue

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1960)
- **Status**: `OPEN`
- **Author**: [@jimmystewpot](https://github.com/jimmystewpot)
- **Created At**: `2026-09-24T03:16:39Z`
- **Updated At**: `2026-10-19T20:29:49Z`
- **Comments**: 3
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1960)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->




### Use Cases

When processing high-volume event streams and large payloads in VRL, several common transformation patterns are currently cumbersome or inefficient:

1. Early Termination (Short-Circuiting): When searching through arrays or objects for a specific element or sentinel condition, we need to halt iteration immediately once found. Currently, iterating through large collections requires scanning every single element even after the target has been matched, wasting significant CPU cycles.
2. Conditional Skipping: Filtering or handling items conditionally during iteration requires deeply nested `if`/`else` blocks rather than a clean imperative `continue`.
3. Ergonomic Imperative Control Flow: Complex event mutations often require traversing and updating nested structures where an imperative loop provides clearer scoping, fewer allocations, and more intuitive error propagation than nested higher-order closures.

### Attempted Solutions

We evaluated and benchmarked the existing mechanisms available in VRL:

### 1. `for_each` closure
Using `for_each` requires iterating through every element, even after finding the matching record:

```vrl
# Searching for a single target record in a large array
found = false
for_each(.,records) -> |_index, record| {
    if !found && record.id == "target-id" {
        .target = record
        found = true
    }
    # Even after found == true, for_each continues running for all remaining elements
}
```
Limitations:
* Unnecessary iteration overhead on large payloads.
* Closures have distinct scoping boundaries; while PR #1931 added a closure-level `break` to `for_each`, it does not provide a native `continue` or the ergonomics of first-class syntax.
* Higher invocation and closure frame overhead compared to a native compiler loop construct.

### 2. Functional combination (filter + indexing)

```vrl
matches = filter(.,records) -> |_index, record| { record.id == "target-id" }
if length(matches) > 0 {
    .target = matches[0]
}
```

Limitations:

* Allocates intermediate array structures in memory.
* Evaluates the entire collection eagerly before returning results.


### Proposal

Introduce native, first-class `for` loop syntax to VRL supporting both arrays and objects with full `break` and `continue` control flow.

### Syntax Examples

```vrl
# 1. Single-item array iteration
for item in .items {
    if item.status == "ignore" {
        continue
    }
    if item.status == "critical" {
        .critical_event = item
        break
    }
}

# 2. Key-value object iteration
for key, value in .metadata {
    if key == "secret" {
        continue
    }
    .sanitized[key] = value
}

# 3. Index-value array iteration
for idx, item in .items {
    .indexed[idx] = item.name
}
```

### Key Capabilities & Semantics

Loop Targets: Support iteration over arrays and objects (both single-item and key-value unpacking).
Control Flow:
Native break and continue statements are validated at compile time (disallowing them outside loop contexts or across closure boundaries).
Non-catchable control flow (Break, Continue, Return) propagating unhindered through ??, ||, and assignments.
Performance & Scoping:
In-place variable slot reuse (ForScopeGuard) restores shadowed variables upon loop exit without hot-loop allocations.
Bounded execution guard via StepBudget to prevent unbounded runtime loops.
Compile-Time Diagnostics: Strict collection type checking rejects non-collection types and invalid union targets with diagnostic error codes (e.g. E630–E635).
Note: A complete implementation covering the compiler, AST, parser (LALRPOP), runtime, benchmarks, and integration test suite is already prepared.

### References

- Draft Implementation PR: https://github.com/vectordotdev/vrl/pull/1952 (`feat(compiler): implement first-class for loops`)
- Initial Discussion: https://github.com/vectordotdev/vrl/discussions/1480 (`break syntax` discussion with maintainer feedback)
- Related PR: https://github.com/vectordotdev/vrl/pull/1931 (`feat(stdlib): add break statement support for early loop exit in for_each`)
