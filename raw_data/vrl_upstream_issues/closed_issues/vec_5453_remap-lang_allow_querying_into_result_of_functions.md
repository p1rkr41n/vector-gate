# Issue #5453: remap-lang: allow querying into result of functions

- **URL:** https://github.com/vectordotdev/vector/issues/5453
- **Author:** @JeanMertz
- **Status:** CLOSED (completed)
- **Created:** 2020-12-09T12:47:48Z
- **Closed:** 2021-02-15T15:40:15Z
- **Labels:** domain:vrl

## Description

We currently support querying the root object using paths (e.g. `.foo.bar`) and also variables (`$foo.bar` since #5094).

We've had at least one report thus far requesting to query the result of functions:

```rust
.url = "https://vector.dev"
.scheme = parse_url(.url).scheme // parse_url returns a `Value::Map`
.scheme // "https"
```

I'm not necessarily advocating we support this (it might be a slippery slope from here to supporting methods, although I don't think that's necessarily the case), but it's worth tracking this, given that more people might be looking for a similar feature.
