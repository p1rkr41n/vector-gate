# [#1471] Syslog rfc5424 parsing does not accept NILVALUE timestamp

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1471)
- **Status**: `OPEN`
- **Author**: [@jinnatar](https://github.com/jinnatar)
- **Created At**: `2025-08-10T13:59:54Z`
- **Updated At**: `2026-06-01T14:08:31Z`
- **Comments**: 4
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1471)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Syslog parsing for rfc5424 rejects a message that does not hold a timestamp and instead uses a NILVALUE, i.e. `-` for that field with the error:
> unable to parse input as valid syslog message

As per the RFC:
> TIMESTAMP       = NILVALUE / FULL-DATE "T" FULL-TIME
  NILVALUE        = "-"

The [TIMESTAMP field guidance 6.2.3](https://www.rfc-editor.org/rfc/rfc5424.html#section-6.2.3) says:
> A syslog application MUST use the NILVALUE as TIMESTAMP if the syslog
   application is incapable of obtaining system time.

My case is exactly this, an embedded device incapable of determining time.

### Configuration

```text
N/A
```

### Version

vector 0.48.0 (x86_64-unknown-linux-gnu a67e4e2 2025-06-30 18:25:45.272082383)

### Debug Output

```text
%> vector vrl --input test-timestamp.json "parse_syslog!(.message)"
2025-08-10T13:53:11.676549Z DEBUG vector::app: Internal log rate limit configured.
2025-08-10T13:53:11.676604Z  INFO vector::app: Log level is enabled. level="trace"
2025-08-10T13:53:11.676717Z DEBUG vector::app: messaged="Building runtime." worker_threads=48
2025-08-10T13:53:11.676828Z TRACE mio::poll: registering event source with poller: token=Token(1), interests=READABLE
{ "appname": "Serial-Debugger", "facility": "user", "hostname": "10.0.4.87", "message": "Serializer started!", "severity": "info", "timestamp": t'2003-08-24T12:14:15.000003Z', "version": 1 }
function call error for "parse_syslog" at (0:23): unable to parse input as valid syslog message
```

### Example Data

```json
{"message":"<14>1 2003-08-24T05:14:15.000003-07:00 10.0.4.87 Serial-Debugger - - - Serializer started!" }
{"message":"<14>1 - 10.0.4.87 Serial-Debugger - - - Serializer started!" }
```

### Additional Context

_No response_

### References

_No response_
