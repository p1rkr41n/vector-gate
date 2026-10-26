# Issue #544: parse_json gives incorrect results for large integers

- **URL:** https://github.com/vectordotdev/vrl/issues/544
- **Author:** @djudd
- **Status:** CLOSED (completed)
- **Created:** 2023-11-03T19:21:30Z
- **Closed:** 2023-11-21T21:50:56Z
- **Labels:** None

## Description

Example: https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoidmFsdWUgPSBcIjkyMjMzNzIwMzY4NTQ3NzU4MDhcIlxuLnBhcnNlZCwgLmVyciA9IHBhcnNlX2pzb24odmFsdWUpIiwiZXZlbnQiOnt9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

input:
```
value = "9223372036854775808"
.parsed, .err = parse_json(value)
```

output:
```
{
	"err": null,
	"parsed": -9223372036854776000
}
```

Some quick experimentation suggests parsing becomes unreliable circa 2^48, but I haven't tested systematically.

(This was found via https://hypothesis.readthedocs.io/en/latest/ tests on my Python code; FWIW I'd suggest using something similar for the parse & encode round-trip in Vector/VRL and might be able to submit that as a contribution if y'all would be interested.)
