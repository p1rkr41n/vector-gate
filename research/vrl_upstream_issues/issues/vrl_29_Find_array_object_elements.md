# [#29] Find array/object elements

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/29)
- **Status**: `OPEN`
- **Author**: [@max-arnold](https://github.com/max-arnold)
- **Created At**: `2022-08-29T09:25:27Z`
- **Updated At**: `2026-06-01T14:17:14Z`
- **Comments**: 3
- **Labels**: `vrl:stdlib`, `good first issue`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/29)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

I'm trying to parse SaltStack logs that contain job results in JSON format. I need to extract the first job argument from a list of positional and keyword arguments.

Given these lists, how to return a first list element that is a string? Or null/failure if the list is empty.

Input

```
[]
["abc"]
[{}, "abc"]
["abc", "def", {"key1":{}, "key2":"val2"}]
```


Output

```
null
abc
abc
abc
```

### Attempted Solutions

A solution proposed by @JeanMertz on Discord looks like this:

```
result = null
for_each(.) -> |_index, value| {
    if result == null && is_string(value) {
        result = value
    }
}

result
```

And this is what I ended up using (just for the reference):

```
.fun_args = []
.fun_kwargs = {}
map_values(array(.data.fun_args) ?? []) -> |v| { if is_string(v) { .fun_args = push(.fun_args, v) } else if is_object(v) { .fun_kwargs = v }}
.first_arg = .fun_args[0]
```

### Proposal

Jean also suggested that this would clearly be a lot easier with a dedicated find enumeration function:

```
# Return the first value in the collection 
# for which the closure returns `true`, or
# return `null` if no match is found.
find(.) -> |_index, value| {
    is_string(value)
}
```

Personally I think this could be generalized to also support objects to find a specific key based on some matching function (like a regex) or to find by value. The primary requirement is being able to use an arbitrary matching expression.

Whether it should return null or fail is up to the VRL language designers.

### References

_No response_

### Version

0.23.3
