# Issue #239: Nested assignment in query can create an invalid type def

- **URL:** https://github.com/vectordotdev/vrl/issues/239
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2023-05-12T20:30:06Z
- **Closed:** 2023-05-26T01:35:39Z
- **Labels:** vrl:typedef, fuzz

## Description

The following VRL code creates an invalid type definition

```coffee
$ type_def(.)
{ "object": {  }, "object_unknown_infinite": { "any": true } }

$ {. =null}.y
null

$ .
null

$ type_def(.)
{ "object": {  }, "object_unknown_infinite": { "any": true } }

```

VRL version: `0.4.0`
