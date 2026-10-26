# [#1361] `format_int` bad output type

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1361)
- **Status**: `OPEN`
- **Author**: [@JTKU](https://github.com/JTKU)
- **Created At**: `2025-03-28T10:22:31Z`
- **Updated At**: `2026-06-16T13:09:32Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`, `stdlib:format_int`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1361)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

The output type of `format_int` seems to be `integer` instead of `string`.

Probably caused by its `TypeDef` being `integer` instead of `bytes`:  [https://github.com/vectordotdev/vrl/blob/07cd43a353829851c899f4fed4edb41a002bb8d1/src/stdlib/format_int.rs#L103](https://github.com/vectordotdev/vrl/blob/07cd43a353829851c899f4fed4edb41a002bb8d1/src/stdlib/format_int.rs#L103)

Since the tests also use the same `TypeDef::integer()` type : [https://github.com/vectordotdev/vrl/blob/07cd43a353829851c899f4fed4edb41a002bb8d1/src/stdlib/format_int.rs#L147](https://github.com/vectordotdev/vrl/blob/07cd43a353829851c899f4fed4edb41a002bb8d1/src/stdlib/format_int.rs#L147), they actually pass, even though declared types are different from that of the actual values.

This is also in contradiction with vector's documentation:  [https://github.com/vectordotdev/vector/blob/2a85007ce5c0ea05cdb408f4d6c898049c33f055/website/cue/reference/remap/functions/format_int.cue#L27](https://github.com/vectordotdev/vector/blob/2a85007ce5c0ea05cdb408f4d6c898049c33f055/website/cue/reference/remap/functions/format_int.cue#L27).

### VRL Program

```text
b, err_b = format_int(.b.value, 2)
c, err_c = to_string(.c.value)

# both are considered strings
.b.is_string = is_string(b)
.c.is_string = is_string(c)

# not ints
.b.is_int = is_integer(b)
.c.is_int = is_integer(c)

# cannot fail so no error catching needed
if is_null(err_c) {
   .c.string = string(c)
}

# can fail, although its return type is the same as `to_string`
if is_null(err_b) {
   .b.string = string(b)
}
```

### VRL and/or Vector Version

vrl 0.22  (vector 0.45.0)

### Debug Output

```text
error[E103]: unhandled fallible assignment
   ┌─ :19:16
   │
19 │    .b.string = string(b)
   │    ----------- ^^^^^^^^^ this expression is fallible because at least one argument's type cannot be verified to be valid
   │    │
   │    or change this to an infallible assignment:
   │    .b.string, err = string(b)
   │
   = see documentation about error handling at https://errors.vrl.dev/#handling
   = see functions characteristics documentation at https://vrl.dev/expressions/#function-call-characteristics
   = learn more about error code 103 at https://errors.vrl.dev/103
   = see language documentation at https://vrl.dev
   = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

### Example

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiYiwgZXJyX2IgPSBmb3JtYXRfaW50KC5iLnZhbHVlLCAyKVxuYywgZXJyX2MgPSB0b19zdHJpbmcoLmMudmFsdWUpXG5cbiMgYm90aCBhcmUgY29uc2lkZXJlZCBzdHJpbmdzXG4uYi5pc19zdHJpbmcgPSBpc19zdHJpbmcoYilcbi5jLmlzX3N0cmluZyA9IGlzX3N0cmluZyhjKVxuXG4jIG5vdCBpbnRzXG4uYi5pc19pbnQgPSBpc19pbnRlZ2VyKGIpXG4uYy5pc19pbnQgPSBpc19pbnRlZ2VyKGMpXG5cbiMgY2Fubm90IGZhaWwgc28gbm8gZXJyb3IgY2F0Y2hpbmcgbmVlZGVkXG5pZiBpc19udWxsKGVycl9jKSB7XG4gICAuYy5zdHJpbmcgPSBzdHJpbmcoYylcbn1cblxuIyBjYW4gZmFpbCwgYWx0aG91Z2ggaXRzIHJldHVybiB0eXBlIGlzIHRoZSBzYW1lIGFzIGB0b19zdHJpbmdgXG5pZiBpc19udWxsKGVycl9iKSB7XG4gICAuYi5zdHJpbmcsIC5iLmVyciA9IHN0cmluZyhiKVxufVxuXG4iLCJldmVudCI6eyJiIjp7InZhbHVlIjo1fSwiYyI6eyJ2YWx1ZSI6NX19LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

### Additional Context

_No response_

### References

Possible solution: [https://github.com/JTKU/vrl/tree/fix_format_int_output_type](https://github.com/JTKU/vrl/tree/fix_format_int_output_type)
