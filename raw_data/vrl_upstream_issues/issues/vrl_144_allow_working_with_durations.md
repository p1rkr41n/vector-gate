# [#144] allow working with durations

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/144)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2020-12-15T13:13:34Z`
- **Updated At**: `2026-06-01T14:16:05Z`
- **Comments**: 1
- **Labels**: `vrl:syntax`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/144)

---

## Description

I wonder if manipulating timestamps is common enough in events that it'd be worth introducing a _duration_ type in the language itself.

For example, one could write:

```rust
.dt = to_timestamp(.dt) + 10s
```

The `<integer>s` part is the type that defines a duration (in this case in seconds). We'd support more than just seconds. Alternative notations are possible (including [ISO8601 duration format](https://en.wikipedia.org/wiki/ISO_8601#Durations)).

Of course, an alternative would be to just allow adding seconds to timestamps:

```rust
.dt = to_timestamp(.dt) + 10 // seconds
```

Or having a `duration` function that takes an integer or float, and a unit of time, and converts that to seconds (or milliseconds, or whatever):

```rust
$hours = 10
.dt = to_timestamp(.dt) + duration($hours, "hour")
```

Of course, it's worth mentioning we already have a [`parse_duration`](https://github.com/timberio/vector/blob/1d3b7c1814dc33a29126e0ecbc217d54646b04a8/src/remap/function/parse_duration.rs) function, which might be "just enough" to cover the basic use cases and there's very little demand for anything more advanced.
