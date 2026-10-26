# Issue #1475: `validate_json_schema` should return validation errors

- **URL:** https://github.com/vectordotdev/vrl/issues/1475
- **Author:** @sbalmos
- **Status:** CLOSED (completed)
- **Created:** 2025-08-13T20:10:41Z
- **Closed:** 2025-09-03T16:06:06Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

The new `validate_json_schema` function, which uses the `jsonschema` crate for its implementation, currently only returns a Boolean `true` or `false` for validation. The function is defined as fallible, however, with provision to return runtime errors. The function should collect the specific validation error(s) returned by the schema validator, and return them in a function error string if validation fails.

### Attempted Solutions

`valid, err = validate_json_schema(s'{"hi":1}', "test-schema.json")` where `test-schema.json` is:
```
{
  "$schema": "https://json-schema.org/draft/2020-12/schema",
  "properties": {
    "id": {
      "type": "string"
    },
    "more": {
      "type": "object",
      "properties": {
        "test": {
          "type": "boolean"
        }
      },
      "required": ["test"],
      "additionalProperties": false
    }
  },
  "required": ["id", "more"],
  "additionalProperties": false
}
```

The current returned value for `valid` is `false` with `err` value `null`.

### Proposal

Validate using `validator.iter_errors(&json)` call, and map/collect any validation errors into a string error message to return. If the string is empty, the JSON passed validation, so return `true`. The current implementation calls `validator.is_valid(&json)`, which only returns the current Boolean `true` / `false` with no indication of the validation error(s).

### References

https://docs.rs/jsonschema/latest/jsonschema/
