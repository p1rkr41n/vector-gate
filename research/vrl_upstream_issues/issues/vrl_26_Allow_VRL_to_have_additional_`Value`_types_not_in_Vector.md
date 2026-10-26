# [#26] Allow VRL to have additional `Value` types not in Vector

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/26)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-09-09T19:29:34Z`
- **Updated At**: `2023-03-28T13:13:49Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/26)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Previously Vector and VRL had entirely separate `Value` types, since VRL has more types (such as regex) than Vector natively supports. These types were merged into a single `Value` type that contains all of the possible options to reduce the performance bottleneck of converting between the types. This is fast, but requires Vector itself to handle any type that VRL might want to have. (e.g. regex)

I propose that these are split again (but differently). VRL gets it's own `Value` type that can contain any type valid in VRL. There will also be a `Value` type shared between the `Target` (e.g. Vector) and VRL, which is a subset of what VRL can support (basically just the JSON types). This allows VRL to have additional types that don't need to be supported by the `Target`, while still allowing fast conversions between the two types.

In order for this to work, VRL specific types will be restricted to local variables only in VRL, and can't be assigned to any external target.

Types will be checked at (VRL) compile time to ensure the following can't be assigned to external values, so type conversion won't need to happen at runtime
- local variables (or queries pointing to local variables) that _ever_ contain VRL specific types (before or after an attempted external assignment.) (This could potentially be relaxed a bit depending on the implementation)
- function return values that could potentially contain VRL specific types
- literals that are VRL specific types

An example that could take advantage of allowing new types is https://github.com/vectordotdev/vrl/issues/25

### Version

0.24.0
