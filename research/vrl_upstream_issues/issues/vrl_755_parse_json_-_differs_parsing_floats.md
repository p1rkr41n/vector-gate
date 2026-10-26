# [#755] parse_json - differs parsing floats

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/755)
- **Status**: `OPEN`
- **Author**: [@guusvw](https://github.com/guusvw)
- **Created At**: `2024-03-20T13:57:33Z`
- **Updated At**: `2026-06-16T13:10:09Z`
- **Comments**: 2
- **Labels**: `vrl:stdlib`, `stdlib:parse_json`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/755)

---

## Description

Hey dear VRL-folks 👋 
I hope this is not a double posting, I only found issues regards `parse_json` for large ints, I'm having an issues as well for floats.

We're getting a JSON which contains the field `ts` and has in our test case the value `1626175065.5934923`
after passing it to `parse_json` the object has the value of `1626175065.5934925`, the last digit differs by 2.
I know, floats are hard & annoying, but is there some way to avoid/fix it?

```
$ message = "{\"level\":\"info\",\"ts\":1626175065.5934923,\"msg\":\"|200|   32.603µs /healthcheck\",\"statusCode\":200,\"request\":306,\"latency\":0.000032603,\"avgLatency\":0.004298489,\"ipPort\":\"1.1.1.1:12345\",\"method\":\"GET\",\"host\":\"1.1.1.1:8080\",\"path\":\"/healthcheck\",\"referer\":\"\"}"
"{\"level\":\"info\",\"ts\":1626175065.5934923,\"msg\":\"|200|   32.603µs /healthcheck\",\"statusCode\":200,\"request\":306,\"latency\":0.000032603,\"avgLatency\":0.004298489,\"ipPort\":\"1.1.1.1:12345\",\"method\":\"GET\",\"host\":\"1.1.1.1:8080\",\"path\":\"/healthcheck\",\"referer\":\"\"}"

$ obj, err = parse_json(message)

{ "avgLatency": 0.004298489, "host": "1.1.1.1:8080", "ipPort": "1.1.1.1:12345", "latency": 0.000032603, "level": "info", "method": "GET", "msg": "|200|   32.603µs /healthcheck", "path": "/healthcheck", "referer": "", "request": 306, "statusCode": 200, "ts": 1626175065.5934925 }
```

```
❯ bin/vector-0.36.1 --version
vector 0.36.1 (x86_64-apple-darwin 2857180 2024-03-11 14:32:52.417737479)
```
