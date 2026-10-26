# [#578] Add support for parsing ndjson

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/578)
- **Status**: `OPEN`
- **Author**: [@dekelpilli](https://github.com/dekelpilli)
- **Created At**: `2023-11-23T05:24:11Z`
- **Updated At**: `2026-06-01T14:18:21Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/578)

---

## Description

I've recently come across a problem that would be more conveniently solved if I could parse ndjson strings within VRL. This could also extend to concatenated JSONs (e.g. `{"a":1}{"a":2}`), or JSONs with a delimiter other than newlines.

I'm not sure exactly what would be the best approach for this feature would be, but I guess it would likely be one of the following:
```coffee
s = s'{"a":1}\n{"a":2}\n0'

parse_json!(s, format: 'ndjson') # [{"a":1}, {"a": 2}, 0]

# or 

parse_json_stream!(s, delimiter: '\n') # [{"a":1}, {"a": 2}, 0]
parse_json_stream!(s'{"a":3}{"a":4}0') # [{"a":3}, {"a": 4}, 0]
```

You can achieve something similar with the `split` +`parse_json` function, but that doesn't fail fast on JSONs across lines: `{"a":"sentence"}\n{"a":"sentence\nwith\nnewlines"}`, and doesn't help with parsing JSON streams with no delimiter (e.g. `{"a":1}{"a":2}`)
