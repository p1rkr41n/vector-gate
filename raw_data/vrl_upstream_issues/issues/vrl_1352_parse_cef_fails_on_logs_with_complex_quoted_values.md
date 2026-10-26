# [#1352] parse_cef fails on logs with complex quoted values

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1352)
- **Status**: `OPEN`
- **Author**: [@unitednf24](https://github.com/unitednf24)
- **Created At**: `2025-03-22T02:18:37Z`
- **Updated At**: `2026-06-16T13:09:34Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:parse_cef`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1352)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

Some CEF logs (specifically from PaloAlto) contain complex key-value pairs in the extension section that cause parsing failures. The problem occurs with fields that contain quoted values with embedded equals signs.

`msg="Example text 0123456789.example.com due to connection failed. subject=/C=US/ST=Example/L=Example/O=Example Home, Incorporated/CN=0123456789.example.com; issuer=/C=US/O=DigiCert Inc/CN=DigiCert Global G2 TLS RSA SHA256 2020 CA1; not before=Oct 7 00:00:00 2024 GMT; not after=Oct 25 23:59:59 2025 GMT; certificate status=Valid;"`

The parser fails with this error: `Error parsing line: Could not parse whole line successfully`

Full CEF log example that causes the error:
`CEF:0|Palo Alto Networks|PAN-OS|10.11.12-h13|test|SYSTEM|5|rt=Jan 01 2025 00:00:00 GMT deviceExternalId=0123456789 cs3Label=Virtual System cs3= fname= flexString2Label=Module flexString2=general msg="Example text 0123456789.example.com due to connection failed. subject=/C=US/ST=Example/L=Example/O=Example Home, Incorporated/CN=0123456789.example.com; issuer=/C=US/O=DigiCert Inc/CN=DigiCert Global G2 TLS RSA SHA256 2020 CA1; not before=Oct 7 00:00:00 2024 GMT; not after=Oct 25 23:59:59 2025 GMT; certificate status=Valid;" externalId=1234567890123456789 cat= PanOSDGl1=0 PanOSDGl2=0 PanOSDGl3=0 PanOSDGl4=0 PanOSVsysName= dvchost=12345 PanOSActionFlags=0x8000000000000000`

Unfortunately, I can't change anything to prevent the generation of these values that contain quoted values with embedded equals signs.

### VRL Program

```text
.cef_message = join!([.appname, ":", .message])
parsed_cef, err = parse_cef(.cef_message)
if err != null {
  log("Unable to parse CEF event" + err, level: "error")
  log(.cef_message, level: "error")
} else {
  . = merge(., parsed_cef)
  del(.cef_message)
  del(.message)
}
```

### VRL and/or Vector Version

0.45.0

### Debug Output

```text

```

### Example

[VRL Playground](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLmNlZl9tZXNzYWdlID0gam9pbiEoWy5hcHBuYW1lLCBcIjpcIiwgLm1lc3NhZ2VdKVxucGFyc2VkX2NlZiA9IHBhcnNlX2NlZiEoLmNlZl9tZXNzYWdlKVxuIiwiZXZlbnQiOnsibWVzc2FnZSI6IjB8UGFsbyBBbHRvIE5ldHdvcmtzfFBBTi1PU3wxMC4xMS4xMi1oMTN8dGVzdHxTWVNURU18NXxydD1KYW4gMDEgMjAyNSAwMDowMDowMCBHTVQgZGV2aWNlRXh0ZXJuYWxJZD0wMTIzNDU2Nzg5IGNzM0xhYmVsPVZpcnR1YWwgU3lzdGVtIGNzMz0gZm5hbWU9IGZsZXhTdHJpbmcyTGFiZWw9TW9kdWxlIGZsZXhTdHJpbmcyPWdlbmVyYWwgbXNnPVwiRXhhbXBsZSB0ZXh0IDAxMjM0NTY3ODkuZXhhbXBsZS5jb20gZHVlIHRvIGNvbm5lY3Rpb24gZmFpbGVkLiBzdWJqZWN0PS9DPVVTL1NUPUV4YW1wbGUvTD1FeGFtcGxlL089RXhhbXBsZSBIb21lLCBJbmNvcnBvcmF0ZWQvQ049MDEyMzQ1Njc4OS5leGFtcGxlLmNvbTsgaXNzdWVyPS9DPVVTL089RGlnaUNlcnQgSW5jL0NOPURpZ2lDZXJ0IEdsb2JhbCBHMiBUTFMgUlNBIFNIQTI1NiAyMDIwIENBMTsgbm90IGJlZm9yZT1PY3QgNyAwMDowMDowMCAyMDI0IEdNVDsgbm90IGFmdGVyPU9jdCAyNSAyMzo1OTo1OSAyMDI1IEdNVDsgY2VydGlmaWNhdGUgc3RhdHVzPVZhbGlkO1wiIGV4dGVybmFsSWQ9MTIzNDU2Nzg5MDEyMzQ1Njc4OSBjYXQ9IFBhbk9TREdsMT0wIFBhbk9TREdsMj0wIFBhbk9TREdsMz0wIFBhbk9TREdsND0wIFBhbk9TVnN5c05hbWU9IGR2Y2hvc3Q9MTIzNDUgUGFuT1NBY3Rpb25GbGFncz0weDgwMDAwMDAwMDAwMDAwMDAiLCJhcHBuYW1lIjoiQ0VGIn0sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9)

### Additional Context

This issue can be resolved using modified version of parse_value function in the /src/stdlib/parse_cef.rs: 
```
fn parse_value(input: &str) -> IResult<&str, String, VerboseError<&str>> {
    if input.starts_with('"') {
        let mut i = 1;
        let mut escaped = false;
        
        while i < input.len() {
            let ch = input[i..].chars().next().unwrap();
            if escaped {
                escaped = false;
            } else if ch == '\\' {
                escaped = true;
            } else if ch == '"' {
                let value = &input[..=i];
                return Ok((&input[i+1..], value.to_string()));
            }
            i += ch.len_utf8();
        }
        return Ok(("", input.to_string()));
    } else {
        alt((
            map(peek(parse_key), |_| String::new()),
            escaped_transform(
                take_till1_input(|input| alt((tag("\\"), tag("="), parse_key))(input).is_ok()),
                '\\',
                alt((
                    value('=', char('=')),
                    value('\\', char('\\')),
                    value('\n', one_of("nr")),
                    success('\\'),
                )),
            ),
        ))(input)
    }
}
```
I'm not a Rust programmer, so this might be the worst block of Rust code in the world.

[CEF_example1.txt](https://github.com/user-attachments/files/19399735/CEF_example1.txt)

### References

_No response_
