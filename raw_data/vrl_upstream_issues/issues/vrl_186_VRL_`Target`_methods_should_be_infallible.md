# [#186] VRL `Target` methods should be infallible

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/186)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-08-10T14:17:05Z`
- **Updated At**: `2026-06-01T14:06:11Z`
- **Comments**: 3
- **Labels**: `type:enhancement`, `vrl:compiler`, `vrl:typedef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/186)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Today, the `Target` trait has 4 methods.

```rust
    fn target_insert(...) -> Result<(), String>;
    fn target_get(...) -> Result<Option<&Value>, String>;
    fn target_get_mut(...) -> Result<Option<&mut Value>, String>;
    fn target_remove(...) -> Result<Option<Value>, String>;
```

All four of these are fallible, however none of the implementations should actually be able to fail at runtime. The VRL type system expects these to always succeed, so any failures can result in invalid type definitions. All of these functions should be modified to be infallible.

There are some places these can still fail at runtime, but the errors are just silently ignored. This is mostly around metrics insertion. This can be solved by adding more compile-time type information to move the errors to compile-time (such as defining "assignable types" and only allowing assignments that match the correct type)


### Version

0.23.0
