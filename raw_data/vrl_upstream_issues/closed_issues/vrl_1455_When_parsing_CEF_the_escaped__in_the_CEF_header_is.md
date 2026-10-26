# Issue #1455: When parsing CEF, the escaped | in the CEF header is not parsed correctly

- **URL:** https://github.com/vectordotdev/vrl/issues/1455
- **Author:** @esmelnikov
- **Status:** CLOSED (completed)
- **Created:** 2025-07-30T15:59:43Z
- **Closed:** 2025-08-05T06:02:24Z
- **Labels:** vrl:stdlib

## Description

If a pipe (|) is used in the header, it must be escaped with a backslash (\). But note that the pipes in the extension do not need escaping. For example:

`{
	"message": "CEF:1|Product|Vendor|7|operation1\\|operation2|Information|Unknown|eventId=7685828129 msg=MessageTest"
}`

Result `. = parse_cef!(.message)` on https://playground.vrl.dev:

`{
	"cefVersion": "1",
	"deviceEventClassId": "operation1|operation2",
	"deviceProduct": "Vendor",
	"deviceVendor": "Product",
	"deviceVersion": "7",
	"eventId": "7685828129",
	"msg": "Message",
	"name": "Information",
	"severity": "Unknown"
}`

The same message processed by vector 0.48.0 (x86_64-pc-windows-msvc a67e4e2 2025-06-30 18:25:45.272082383) gives the following result:

`{
	"cefVersion": "1",
	"deviceEventClassId": "operation1\\",
	"deviceProduct": "Vendor",
	"deviceVendor": "Product",
	"deviceVersion": "7",
	"eventId": "7685828129",
	"msg": "Message",
	"name": "Information",
}`
