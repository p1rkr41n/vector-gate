# Issue #648: Feature request: decode_protobuf  (parse_protobuf?)

- **URL:** https://github.com/vectordotdev/vrl/issues/648
- **Author:** @johnhtodd
- **Status:** CLOSED (completed)
- **Created:** 2024-01-22T21:09:13Z
- **Closed:** 2024-03-26T13:57:24Z
- **Labels:** vrl:stdlib

## Description

We have found ourselves in a situation where there is protobuf messaging being encoded into a field inside another protobuf message.  There are a variety of helpful features in Vector now that perform "decode" functions on data-within-data, but not something that I can currently see which would decode protobuf messages embedded into objects.  Perhaps this might be useful to others as well.

I would expect a definition (file path?) of the .proto file would have to be provided as part of the function call.

(would a better term here be "parse_protobuf" instead of "decode_protobuf"?  I'm not sure where each term would be applied in this situation.)

To be entirely feature complete, it would be ideal for a patch be able to put protobuf messages back into protobuf fields, but that is not something we need to do and we would be ENTIRELY satisfied to have it just be a decode process and not an encode process as well.  :-)
