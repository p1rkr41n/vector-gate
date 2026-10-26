# Issue #799: VRL is unable to transform base62 encoded 128-bit identifiers to UUIDs

- **URL:** https://github.com/vectordotdev/vrl/issues/799
- **Author:** @andrewthad
- **Status:** CLOSED (completed)
- **Created:** 2024-04-15T17:33:25Z
- **Closed:** 2024-04-19T20:51:43Z
- **Labels:** vrl:stdlib

## Description

Some software encodes 128-bit UUIDs using base62, but a lot of software expects to see the traditional hyphenated base16 encoding of these identifiers. A user currently needs to fallback to lua for this since VRL is unable to perform the transformation. It would be helpful  to have a function `uuidFromBase62` that takes a string argument and returns a string (with the possibility of failure). Here is a concrete example of the expected behavior:

```
Argument: "3s87yEvnmkiPBMHsj8bwwc"
Result: "7f41deed-d5e2-8b5e-7a13-ab4ff93cfad2"
```

Failure should occur in any of these cases:

* the byte sequence represented by the argument is more than 16 bytes long
* the arguments contains characters not in the class `[0-9A-Za-Z]`

I'm probably going to need to roll this on my own soon so that I can get data into clickhouse (which expects UUIDs as hyphenated base16 json strings). I would appreciate any feedback on the name or overall design, or any feedback that would make it more likely that would increase the likelihood that I can upstream this work. Thanks.
