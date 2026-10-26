# [#1454] Function parse_cef() does not parsed the string, but on playground.vrl.dev website the message is parsed

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1454)
- **Status**: `OPEN`
- **Author**: [@esmelnikov](https://github.com/esmelnikov)
- **Created At**: `2025-07-30T14:35:50Z`
- **Updated At**: `2026-06-01T14:08:30Z`
- **Comments**: 1
- **Labels**: `stdlib:parse_cef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1454)

---

## Description

### A note for the community

Message for parsed:
`{
	"message": "CEF:1|Microsoft|Microsoft Windows WMI Activity||Microsoft-Windows-WMI-Activity:5857|Microsoft-Windows-WMI-Activity|Low|eventId=10223573 externalId=5857 start=1753856830316 end=1753856830316 art=1753856959017 cat=Microsoft-Windows-WMI-Activity/Operational deviceSeverity=Information rt=1753856830316 duser=NETWORK SERVICE oldFileHash=en_US|UTF-8 cs1={\"Operation_StartedOperational\":{\"@_xmlns_\":\"http://manifests.microsoft.com/win/2006/windows/WMI\",\"ProviderName\":\"Win32_WIN32_TERMINALSERVICE_Prov\",\"Code\":\"0x0\",\"HostProcess\":\"wmiprvse.exe\",\"ProcessID\":\"7080\",\"ProviderPath\":\"%SystemRoot%\\system32\\tscfgwmi.dll\"}} cs2=None cs3=Microsoft-Windows-WMI-Activity cs2Label=EventlogCategory cs3Label=UserData ahost=abc.abc.abc.net agt=10.10.10.10 agentZoneURI=/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 10.0.0.0-10.255.255.255 amac=40-A6-B7-B8-39-A9 at=winc dvchost=abc.abc.abc.net dvc=10.10.15.13 deviceZoneURI=/All Zones/ArcSight System/Private Address Space Zones/RFC1918: 172.16.0.0-172.31.255.255 _cefVer=1.0 ad.EventRecordID=277537 ad.Version=0 ad.ThreadID=20360 ad.Opcode=Info ad.ProcessID=7080 aid=39u1FgJEBABCACHtAUahVXQ\\=\\="
}`


### Problem

Function parse_cef() does not parsed the string, but on playground.vrl.dev website the message is parsed

### VRL Program

```text
transforms:
  decode_cef:
    type: remap
    inputs: ["kafka_cef"]
    source: |
        messagecef = string!(.message)
        del(.)
        messagecef = replace!(messagecef, "| ", "|")
        parsedcef, err = parse_cef(messagecef, translate_custom_fields: true)
        .parsed77 = parsedcef
        if err == null {
            .parsed77 = parsedcef
            .source77 = messagecef
        } else {
            .error77 = messagecef
            log("CEF RAW: " + string!(messagecef))
        }
```

### VRL and/or Vector Version

vector 0.48.0 (x86_64-pc-windows-msvc a67e4e2 2025-06-30 18:25:45.272082383)

### Debug Output

```text

```

### Example

https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLiA9IHBhcnNlX2NlZiEoLm1lc3NhZ2UpIiwiZXZlbnQiOnsibWVzc2FnZSI6IkNFRjoxfE1pY3Jvc29mdHxNaWNyb3NvZnQgV2luZG93cyBXTUkgQWN0aXZpdHl8fE1pY3Jvc29mdC1XaW5kb3dzLVdNSS1BY3Rpdml0eTo1ODU3fE1pY3Jvc29mdC1XaW5kb3dzLVdNSS1BY3Rpdml0eXxMb3d8ZXZlbnRJZD0xMDIyMzU3MyBleHRlcm5hbElkPTU4NTcgc3RhcnQ9MTc1Mzg1NjgzMDMxNiBlbmQ9MTc1Mzg1NjgzMDMxNiBhcnQ9MTc1Mzg1Njk1OTAxNyBjYXQ9TWljcm9zb2Z0LVdpbmRvd3MtV01JLUFjdGl2aXR5L09wZXJhdGlvbmFsIGRldmljZVNldmVyaXR5PUluZm9ybWF0aW9uIHJ0PTE3NTM4NTY4MzAzMTYgZHVzZXI9TkVUV09SSyBTRVJWSUNFIG9sZEZpbGVIYXNoPWVuX1VTfFVURi04IGNzMT17XCJPcGVyYXRpb25fU3RhcnRlZE9wZXJhdGlvbmFsXCI6e1wiQF94bWxuc19cIjpcImh0dHA6Ly9tYW5pZmVzdHMubWljcm9zb2Z0LmNvbS93aW4vMjAwNi93aW5kb3dzL1dNSVwiLFwiUHJvdmlkZXJOYW1lXCI6XCJXaW4zMl9XSU4zMl9URVJNSU5BTFNFUlZJQ0VfUHJvdlwiLFwiQ29kZVwiOlwiMHgwXCIsXCJIb3N0UHJvY2Vzc1wiOlwid21pcHJ2c2UuZXhlXCIsXCJQcm9jZXNzSURcIjpcIjcwODBcIixcIlByb3ZpZGVyUGF0aFwiOlwiJVN5c3RlbVJvb3QlXFxzeXN0ZW0zMlxcdHNjZmd3bWkuZGxsXCJ9fSBjczI9Tm9uZSBjczM9TWljcm9zb2Z0LVdpbmRvd3MtV01JLUFjdGl2aXR5IGNzMkxhYmVsPUV2ZW50bG9nQ2F0ZWdvcnkgY3MzTGFiZWw9VXNlckRhdGEgYWhvc3Q9YWJjLmFiYy5hYmMubmV0IGFndD0xMC4xMC4xMC4xMCBhZ2VudFpvbmVVUkk9L0FsbCBab25lcy9BcmNTaWdodCBTeXN0ZW0vUHJpdmF0ZSBBZGRyZXNzIFNwYWNlIFpvbmVzL1JGQzE5MTg6IDEwLjAuMC4wLTEwLjI1NS4yNTUuMjU1IGFtYWM9NDAtQTYtQjctQjgtMzktQTkgYXQ9d2luYyBkdmNob3N0PWFiYy5hYmMuYWJjLm5ldCBkdmM9MTAuMTAuMTUuMTMgZGV2aWNlWm9uZVVSST0vQWxsIFpvbmVzL0FyY1NpZ2h0IFN5c3RlbS9Qcml2YXRlIEFkZHJlc3MgU3BhY2UgWm9uZXMvUkZDMTkxODogMTcyLjE2LjAuMC0xNzIuMzEuMjU1LjI1NSBfY2VmVmVyPTEuMCBhZC5FdmVudFJlY29yZElEPTI3NzUzNyBhZC5WZXJzaW9uPTAgYWQuVGhyZWFkSUQ9MjAzNjAgYWQuT3Bjb2RlPUluZm8gYWQuUHJvY2Vzc0lEPTcwODAgYWlkPTM5dTFGZ0pFQkFCQ0FDSHRBVWFoVlhRXFw9XFw9In0sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9

### Additional Context

_No response_

### References

_No response_
