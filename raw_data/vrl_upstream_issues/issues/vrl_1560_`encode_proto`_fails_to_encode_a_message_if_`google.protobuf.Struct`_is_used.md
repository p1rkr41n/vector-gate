# [#1560] `encode_proto` fails to encode a message if `google.protobuf.Struct` is used

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1560)
- **Status**: `OPEN`
- **Author**: [@simplepad](https://github.com/simplepad)
- **Created At**: `2025-11-20T11:20:09Z`
- **Updated At**: `2026-06-01T14:08:48Z`
- **Comments**: 0
- **Labels**: `stdlib:encode_proto`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1560)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

Trying to encode an object field using a protobuf .desc file generated from a proto file that uses `google.protobuf.Struct` results in an empty protobuf map.

Example test.proto file:
```proto
syntax = "proto3";

import "google/protobuf/struct.proto";

package test;

message TestMessage {
  google.protobuf.Struct data = 1;
}
```

Compile it into a .desc file using `protoc -o test.desc --include_imports test.proto`

Example vector config:
```yaml
sources:
  in:
    type: demo_logs
    format: json
    count: 1
transforms:
  tr:
    type: remap
    inputs:
      - in
    source: |-
      .data = {"hello": "world"}
      .encoded_proto = encode_base64!(encode_proto!(., "test.desc", "test.TestMessage"))
sinks:
  out:
    type: console
    inputs:
      - tr
    encoding:
      codec: json
```

Observe the `encoded_proto` field in the output. Try to decode it using an external protobuf decoder (for example cyberchef). The encoded protobuf only contains an empty map.

It might be that the code needs special handling for google structs.
https://github.com/vectordotdev/vrl/blob/bddc7868c707651beef4c875f857b505f5e1a695/src/protobuf/encode.rs#L98-L121

### VRL Program

```text

```

### VRL and/or Vector Version

latest commit on the main branch

### Debug Output

```text

```

### Example

_No response_

### Additional Context

_No response_

### References

_No response_
