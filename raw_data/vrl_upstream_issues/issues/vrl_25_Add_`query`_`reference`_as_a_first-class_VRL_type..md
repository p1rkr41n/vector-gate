# [#25] Add `query`/`reference` as a first-class VRL type.

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/25)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-09-09T19:51:47Z`
- **Updated At**: `2026-06-01T14:17:19Z`
- **Comments**: 3
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/25)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Today the syntax for "reading a value from an object", and "a query path referencing a field of an object" are identical.

### Examples
query an object
```coffee
. = {"foo": {"bar": 3}}
x = .foo.bar
# x is 3
```

delete a field
```coffee
. = {"foo": {"bar": 3}}

# the function arg is treated as a "query". The value 3 is not passed into the function.
del(.foo.bar)

```



Having a distinct syntax for creating references vs accessing a field could allow more elegant code and reduce confusion here.
As an [example](https://discord.com/channels/742820443487993987/1017219484630651020), a vector user attempted to delete multiple fields in an object by using the following code (which doesn't work):

```coffee
fields = [".source_type", ".kubernetes.pod_ip"]
for_each(fields) -> |_index, value| {
  del(value)
}
```

`fields` here just contains an array of strings, which fails to compile since `del` expects "queries".  If `fields` was switched to
`fields = [.source_type, .kubernetes.pod_ip]`, then it would just contain an array of the _values_ that the query paths point to.

I am proposing that additional syntax is added to create "references", which just point to specific fields/indices of objects/arrays.
This is just a standard query path with `&` appended. For example, `a = &.foo.bar` would mean that the local variable `a` is a reference to `.foo.bar`.  The above invalid example could be re-written with these changes so it would work as expected.

```coffee
fields = [&.source_type, &.kubernetes.pod_ip]
for_each(fields) -> |_index, value| {
  del(value)
}
```

Note that this would require some additional work before it could be it could be implemented:
- https://github.com/vectordotdev/vrl/issues/26


### Version

0.24.0
