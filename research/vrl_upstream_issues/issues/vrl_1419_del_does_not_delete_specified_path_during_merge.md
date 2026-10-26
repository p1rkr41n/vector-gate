# [#1419] del does not delete specified path during merge

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1419)
- **Status**: `OPEN`
- **Author**: [@DimDroll](https://github.com/DimDroll)
- **Created At**: `2025-06-04T12:57:18Z`
- **Updated At**: `2026-06-01T14:08:28Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1419)

---

## Description

### A note for the community

_No response_

### Problem

Hello Vector Team,

Following playground URL shows the issue I'm facing with del function:
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiIy4gfD0gb2JqZWN0IShwYXJzZV9qc29uIShkZWwoLm1lc3NhZ2UpKSlcblxuc29tZXZhciA9IGRlbCgubWVzc2FnZSlcbi4gfD0gb2JqZWN0IShwYXJzZV9qc29uIShzb21ldmFyKSkiLCJldmVudCI6eyJtZXNzYWdlIjoie1wia2V5XCI6XCJmaWVsZFwifSIsImh0dHBfc3RhdHVzIjoiMjAwIn0sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9

Not sure if this is expected behavior or not, but when I have following statement:
`. |= object!(parse_json!(del(.message)))`

with the original event:
```
{
	"message": "{\"key\":\"field\"}",
	"http_status": "200"
}
```
produces (**please note still present "message" field even though I would have expected it to be deleted**):
```
{
	"http_status": "200",
	"key": "field",
	"message": "{\"key\":\"field\"}"
}
```

However, when I have seemingly the same program it gives the needed result:
```
somevar = del(.message)
. |= object!(parse_json!(somevar))
```

You can test this with the link above, I was under impression that single line solution worked before, but I might be mistaken.

### VRL Program

```text
#. |= object!(parse_json!(del(.message)))

somevar = del(.message)
. |= object!(parse_json!(somevar))
```

### VRL and/or Vector Version

0.24.0

### Debug Output

```text

```

### Example

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiIy4gfD0gb2JqZWN0IShwYXJzZV9qc29uIShkZWwoLm1lc3NhZ2UpKSlcblxuc29tZXZhciA9IGRlbCgubWVzc2FnZSlcbi4gfD0gb2JqZWN0IShwYXJzZV9qc29uIShzb21ldmFyKSkiLCJldmVudCI6eyJtZXNzYWdlIjoie1wia2V5XCI6XCJmaWVsZFwifSIsImh0dHBfc3RhdHVzIjoiMjAwIn0sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9

### Additional Context

_No response_

### References

_No response_
