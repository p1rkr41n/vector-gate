# [#1139] Fold enumeration function

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1139)
- **Status**: `OPEN`
- **Author**: [@jakedipity](https://github.com/jakedipity)
- **Created At**: `2024-11-25T18:27:05Z`
- **Updated At**: `2025-01-31T15:19:26Z`
- **Comments**: 2
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1139)

---

## Description

Having a fold function like the rust's [Iterator::fold](https://doc.rust-lang.org/std/iter/trait.Iterator.html#method.fold) would be a nice-to-have for compacting objects array into a single value.

Consider the contrived issue of trying to tally the total count of elements parsed out of a line
```
count(25) count(3) count(42) count(1);
```

This is currently possible but requires side effects to accomplish:
```
matches = parse_regex_all!(.message, r'count\((?<count>\d+)\)')
.count = 0
for_each(matches) -> |_index, value| {
  .count = .count + (to_int(value.count) ?? 0)
}
```

A fold function provides a slightly more terse way to accomplish this.
```
matches = parse_regex_all!(.message, r'count\((?<count>\d+)\)')
.count = fold(matches, 0) -> |accum, _index, value| {
  accum + (to_int(value.count) ?? 0)
}
```

I got ahead of myself and already started working on an [implementation](https://github.com/jakedipity/vrl/commit/e374bd27f7cbf5623cff7f42b48073ebdbf10f23). Assuming you think this function is useful to include in the stdlib, the only thing I'm unsure of now is how to type the accumulator value of the closure.

* The simplest answer is to treat it as `Kind::ANY` but this always requires type assertions and handling within the function.
* My current implementation treats it as the same type as `initial_value`, with some small changes to the internals.
* The ideal seems to be a union between the `initial_value` and closure return type - although this probably requires further changes to the internals
