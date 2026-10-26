# Issue #737: Add `uuid_v7` function

- **URL:** https://github.com/vectordotdev/vrl/issues/737
- **Author:** @ppaulweber
- **Status:** CLOSED (completed)
- **Created:** 2024-03-10T22:16:18Z
- **Closed:** 2024-03-14T19:05:21Z
- **Labels:** None

## Description

Due to the already existing `uuid_v4()` function for randomized UUID generation in format version 4, I would like to use the timestamp based UUID version 7 generation in vector-based `remap` types by just simply calling a VRL function `uuid_v7()` to generate a current UUID v7 identifier.

Moreover, the `uuid_v7()` function shall allow an optional parameter to pass a given timestamp (by default it corresponds to the `now()` function) to generate the randomized portion of the provided timestamp.
