# [#87] VRL: add `parse_json_object` as a convenient way to parse JSON objects

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/87)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2021-11-05T10:16:15Z`
- **Updated At**: `2023-05-02T19:09:28Z`
- **Comments**: 17
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/87)

---

## Description

The `parse_json` function is frequently used to parse the `.message` field into a JSON object. Technically, a string such as `"true"` is also valid JSON, in that it produces the boolean JSON value `true`. Because of this, the return type of the `parse_json` function is any valid JSON type.

This is annoying when you just want to parse the message as a JSON object, e.g.:

```coffee
. |= object!(parse_json!(.message))
```

I propose we add a convenience function `parse_json_object` that fails if the resulting type isn't an object.

This allows you to write:

```coffee
. |= parse_json_object!(.message)
```

Which isn't _much_ shorter, but it is less cluttered with verbose syntax of wrapping two functions.

I also thought of allowing something like `parse_json!(.message, kind: "object")`, but that feels like an awkward interface to have.

Note that there is also the `merge` function, which already works this way because it requires an object as input:

```coffee
. = merge!(., .message) # fails if `.` or `.message` isn't an object
```

But I've seen a sufficient number of people use `. |= ...` in the wild, that it might make sense to optimize that pattern.

I'm also open to alternatives that improve this use-case (perhaps "just" documenting this better could be a first step).
