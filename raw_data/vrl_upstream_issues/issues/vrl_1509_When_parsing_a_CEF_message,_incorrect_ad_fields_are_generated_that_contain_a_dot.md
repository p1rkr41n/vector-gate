# [#1509] When parsing a CEF message, incorrect ad fields are generated that contain a dot in the name

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1509)
- **Status**: `OPEN`
- **Author**: [@esmelnikov](https://github.com/esmelnikov)
- **Created At**: `2025-09-15T12:20:26Z`
- **Updated At**: `2026-06-01T14:08:37Z`
- **Comments**: 0
- **Labels**: `stdlib:parse_cef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1509)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

When parsing a CEF message, incorrect ad fields are generated that contain a dot in the name

### Configuration

```text
.= parse_cef(message, translate_custom_fields: false)
```

### Version

vector 0.49.0 (x86_64-pc-windows-msvc dc7e792 2025-08-12 13:47:08.632326804)

### Debug Output

```text

```

### Example Data

CEF:1|ABC|EFG|4.0.2.0|61682|Application Event|High| eventId=201608131 externalId=447 msg=Jet: A bad page link has been detected start=1757904060000 end=1757904060000 categorySignificance=Error catdt=Log Consolidator art=1757904105331 cat=Application deviceSeverity=8 rt=1757904060000 suser=N/A cs2=N/A locality=0 cs2Label=SIDType cs5Label=ObjectSID cs6Label=ObjectName cn1Label=LogonType _cefVer=1.0 ad.=> 10348, 10349). ad.EventPath=EventPath

### Additional Context

After parsing  cut example "_cefVer":"1.0","ad.":"> 10348, 10349).","ad.EventPath":"EventPath"

### References

_No response_
