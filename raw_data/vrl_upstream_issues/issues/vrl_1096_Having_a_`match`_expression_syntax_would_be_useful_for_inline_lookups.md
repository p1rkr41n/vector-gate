# [#1096] Having a `match` expression syntax would be useful for inline lookups

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1096)
- **Status**: `OPEN`
- **Author**: [@bruceg](https://github.com/bruceg)
- **Created At**: `2024-10-25T17:24:44Z`
- **Updated At**: `2026-06-01T14:18:50Z`
- **Comments**: 0
- **Labels**: `vrl:syntax`, `vrl:compiler`, `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1096)

---

## Description

I am writing some event mapping code that does a number of what are effectively inline table lookups. For example:

```
activity_name = if activity_id == 0 { "Unknown" } else
                if activity_id == 1 { "Open" } else
                if activity_id == 2 { "Close" } else
                if activity_id == 3 { "Reset" } else
                if activity_id == 4 { "Fail" } else
                if activity_id == 5 { "Refuse" } else
                if activity_id == 6 { "Traffic" } else
                { "Other" }
```

I cannot use an object with `get` for this, as sometimes the key is string, integer, or `null`, but objects only have string keys. Also, doing a quick command-line microbenchmark seems to indicate that the above scaffolding is faster than using `get` when the average branch chosen is less than about 7-8 when using strings.

It would be handy to have some way of expressing the above as a series of cases, analogous to C's `switch` statement or Rust's `match` expression:

```
activity_name = match activity_id {
  0 => "Unknown",
  1 => "Open",
  2 => "Close",
  3 => "Reset",
  4 => "Fail",
  5 => "Refuse",
  6 => "Traffic",
  else => "Other",
}
```

Obviously, in C you can't easily do string matches which would be highly desirable, and Rust's syntax is much more sophisticated than would likely be useful for VRL, so some balance would be desirable.
