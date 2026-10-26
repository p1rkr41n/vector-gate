# Issue #1157: Add functions to map an array into an object

- **URL:** https://github.com/vectordotdev/vrl/issues/1157
- **Author:** @bruceg
- **Status:** CLOSED (completed)
- **Created:** 2024-12-02T16:52:27Z
- **Closed:** 2024-12-05T18:07:03Z
- **Labels:** vrl:stdlib

## Description

When manipulating data that has been parsed from CSV or other columnar data sources, it is useful to be able to map those columns into an object with named fields. I propose adding two functions to accomplish this, mirroring the approach in Python: `object` and `zip`:

* `zip` takes a number of arrays as input and produces a single array as output containing a tuple of elements from each array. For example `zip([1,2,3],[4,5,6],[7,8,9])` returns `[[1,4,7],[2,5,8],[3,6,9]]`.
* `object` takes takes a zipped array as above with (key, value) pairs and produces an object as output. For example `object([["foo":1],["bar":2]])` returns `{"foo":1,"bar":2}`.

