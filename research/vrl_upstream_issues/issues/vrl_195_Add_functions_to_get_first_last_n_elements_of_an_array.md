# [#195] Add functions to get first/last n elements of an array

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/195)
- **Status**: `OPEN`
- **Author**: [@Leo1003](https://github.com/Leo1003)
- **Created At**: `2023-04-19T12:10:20Z`
- **Updated At**: `2024-05-17T19:24:30Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/195)

---

## Description

Currently, I cannot find a proper way to limit the length of an array.

I wish there are functions which can return the first or last n elements of an array.

## Example
```
first([0, 1, 2, 3], 3)
// Output: [0, 1, 2]

first([0], 3)
// Output: [0]

last([0, 1, 2, 3], 3)
// Output: [1, 2, 3]

last(["apple", "book", "car", "door"], 2)
// Output: ["car", "door"]
```
