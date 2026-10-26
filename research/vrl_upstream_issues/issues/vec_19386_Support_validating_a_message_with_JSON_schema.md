# [#19386] Support validating a message with JSON schema

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/19386)
- **Status**: `OPEN`
- **Author**: [@blake-mealey](https://github.com/blake-mealey)
- **Created At**: `2023-12-14T15:03:23Z`
- **Updated At**: `2026-05-30T00:09:33Z`
- **Comments**: 3
- **Labels**: `domain:processing`, `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/19386)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

We're using vector as a usage event pipeline. We currently define JSON schemas for each of our event types which we can use to validate events at write time. However, we've been considering using Vector as the entrypoint for some new event types (creating events from an S3 bucket which uses a different format). For this case, it would be nice to transform the data into the correct shape, and then have the pipeline validate it against a schema to ensure it's correct. 

### Attempted Solutions

So far we haven't attempted anything, but if first-class support is not added, I think I will attempt to write a tool that generates a VRL script to validate an event against a JSON schema.

### Proposal

1. A new global configuration which defines where to load JSON schemas from (similar to `enrichment_tables`)
2. A new VRL function to validate a value against a JSON schema by name

For example, the global configuration may look like:

```yaml
schemas:
  my_schema:
    type: json_schema
    file_path: /vector-config/schemas/my_schema.json
```

And the VRL function usage might look like:

```vrl
is_valid, err = validate_schema(., 'my_schema')
```

### References

_No response_

### Version

_No response_
