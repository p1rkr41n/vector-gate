# Issue #103: Cannot Parse HTTP Error Log with parse_apache_log

- **URL:** https://github.com/vectordotdev/vrl/issues/103
- **Author:** @jszwedko
- **Status:** CLOSED (completed)
- **Created:** 2021-07-23T14:12:00Z
- **Closed:** 2024-12-24T22:06:01Z
- **Labels:** vrl:stdlib

## Description

### Discussed in https://github.com/timberio/vector/discussions/8429

<div type='discussions-op-text'>

<sup>Originally posted by **tastyfrankfurt** July 22, 2021</sup>
Having issues with the parse_apache_log parser doesnt like our error logs, see below for example,
$ parse_apache_log!(s'[Fri Jul 23 00:28:19.615325 2021] [:error] [pid 17705] ipa: INFO: [jsonserver_session] fred@example.local: idview_show(None, version=u\\'2.237\\'): RequirementError', timestamp_format:"%a %b %d %H:%M:%S.%6f %Y", format: "error")
function call error for "parse_apache_log" at (0:246): failed parsing common log line

Thanks

Tasty</div>
