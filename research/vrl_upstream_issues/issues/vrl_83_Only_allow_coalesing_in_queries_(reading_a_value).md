# [#83] Only allow coalesing in queries (reading a value)

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/83)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-01-20T15:52:00Z`
- **Updated At**: `2023-06-21T13:44:15Z`
- **Comments**: 2
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/83)

---

## Description

Currently, path coalescing can be used in any location in VRL that expects a so-called `Query` expression.

For example, fetching a field from the external target using coalescing would be done as:

```json
{ "foo": { "baz": true } }
```

```coffee
.foo.(bar | baz)
```

```json
true
```

This is a non-ambigious example, but the ambiguity happens when you use paths for non-query related work, such as deleting a field:

```
{ "foo": { "bar": true, "baz": true } }
```

```coffee
del(.foo.(bar | baz))
```

The below could be interpreted in different ways:

```jsonc
// remove first found element
{ "foo": { "baz": true } }
// remove last found element
{ "foo": { "bar": true } }
// remove all found element
{ "foo": { } }
```

The same applies for operations where we _insert_ information based on a path.

We've had discussions in the past on whether we should remove path coalescing entirely, but @lukesteensen rightfully brought up the fact that we could instead restrict its usage in non-query use-cases. So, the above `del` function call would be invalid because the provided path uses coalescing.
