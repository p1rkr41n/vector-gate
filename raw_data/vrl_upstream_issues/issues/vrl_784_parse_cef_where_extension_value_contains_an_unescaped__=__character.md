# [#784] parse_cef where extension value contains an unescaped "=" character

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/784)
- **Status**: `OPEN`
- **Author**: [@aacgood](https://github.com/aacgood)
- **Created At**: `2024-04-05T04:00:15Z`
- **Updated At**: `2025-09-15T14:16:42Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:parse_cef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/784)

---

## Description

Hi,

I am trying to parse the following using the `parse_cef` function however it returns error[E000]: function call error for "parse_cef" at (15:35): Could not parse whole line successfully

Note: I've stripped and anon'd the log but the offending part seems to be is in cs67 as it contains a url with an unescaped equals character.

```
{"message":"<114>2024-01-01T00:00:00.000Z MYHOST01 CEF:0|Vendor|Product|2024.7.0.2|DETECT_AND_RESPOND|ENDPOINT|9|cat=\"Endpoint\" cs2Label=incidentID cs2=00000000-0000-0000-0000-000000000000\" cs67Label=callbackURL cs67=\"https://my.domain.goes.here.com/#/incidents?incidentID=000000000-0000-0000-0000-000000000000\" cs68Label=tenantID cs68=INTERNAL "}
```

When I manually update `incidentId=` to be `incidentId\\=` then the parse_cef function works as expected, Whilst the value for cs67 is contained within quotes, it appears to be a bug where it doesnt parse.

As a side note, using the parse_key_value() function is able to extract the unescaped value correctly.  This was tested using Vector 0.36.1 and can be replicated in [VRL playground](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiIyBOYXRpdmUgZnVuY3Rpb24gZmFpbHNcbi50ZXN0MSA9IHBhcnNlX2NlZiEoLm1lc3NhZ2UpXG5cblxuXG5cblxuIyByZXBsYWNpbmcgPSB3aXRoIFxcXFw9IHdvcmtzXG5tYXRjaGVyID0gbWF0Y2goLm1lc3NhZ2UsIHInaW5jaWRlbnRJRD0nKSA%2FPyBmYWxzZVxuXG4jaWYgbWF0Y2hlciB7XG4jICAubWVzc2FnZSwgZXJyID0gcmVwbGFjZSgubWVzc2FnZSwgXCJpbmNpZGVudElEPVwiLCBcImluY2lkZW50SURcXFxcPVwiKVxuI31cbiMudGVzdDIgPSBwYXJzZV9jZWYhKC5tZXNzYWdlKVxuXG5cblxuXG5cblxuIyBUaGUgcGFyc2Vfa2V5X3ZhbHVlIGZ1bmN0aW9uIGFsc28gd29ya3NcbiMudGVzdDMgPSBwYXJzZV9rZXlfdmFsdWUhKC5tZXNzYWdlKSIsImV2ZW50Ijp7Im1lc3NhZ2UiOiI8MTE0PjIwMjQtMDEtMDFUMDA6MDA6MDAuMDAwWiBNWUhPU1QwMSBDRUY6MHxWZW5kb3J8UHJvZHVjdHwyMDI0LjcuMC4yfERFVEVDVF9BTkRfUkVTUE9ORHxFTkRQT0lOVHw5fGNhdD1cIkVuZHBvaW50XCIgY3MyTGFiZWw9aW5jaWRlbnRJRCBjczI9MDAwMDAwMDAtMDAwMC0wMDAwLTAwMDAtMDAwMDAwMDAwMDAwXCIgY3M2N0xhYmVsPWNhbGxiYWNrVVJMIGNzNjc9XCJodHRwczovL215LmRvbWFpbi5nb2VzLmhlcmUuY29tLyMvaW5jaWRlbnRzP2luY2lkZW50SUQ9MDAwMDAwMDAwLTAwMDAtMDAwMC0wMDAwLTAwMDAwMDAwMDAwMFwiIGNzNjhMYWJlbD10ZW5hbnRJRCBjczY4PUlOVEVSTkFMICJ9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D)

Cheers


