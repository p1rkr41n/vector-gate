# Issue #1214: Unused checker reports variable used in if-condition inside for_each block as unused

- **URL:** https://github.com/vectordotdev/vrl/issues/1214
- **Author:** @B-Schmidt
- **Status:** CLOSED (completed)
- **Created:** 2025-01-09T13:40:25Z
- **Closed:** 2025-01-13T15:59:22Z
- **Labels:** vrl:compiler, vrl:expression checker

## Description

In trying to implement a sort of `take_while` construct I have come across a variable being incorrectly marked as unused. Sample code to reproduce:

```vrl
thing = [1, 2,  -1, 3]
.valid = []
done = false

for_each(thing) -> |_i, v| {
    if !done {
        .valid = push(.valid, v)
    }
    if v < 0 {
        done = true
    }
}
```

This results in an `unused variable` warning for the line `done = false` despite the use of `done` in the condition on line 6. Removing the expression as the warning suggests will of course fail to compile due to an undefined variable.
