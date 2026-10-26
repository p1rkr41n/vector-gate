# Issue #241: `undefined` types not handled properly in array literals

- **URL:** https://github.com/vectordotdev/vrl/issues/241
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2023-05-13T01:26:19Z
- **Closed:** 2023-08-18T18:37:35Z
- **Labels:** vrl:typedef, fuzz

## Description

If you create an array where one of the elements is `undefined`, the actual result is an array with a `null` element, but the type definition thinks that element won't exist (an empty array).

```coffee
$ . = {}
{  }

$ [.x]
[null]

$ type_def([.x])
{ "array": {  } }
```
