# Issue #7: "to_timestamp" should recognize TIMESTAMP_ISO8601 grok-pattern

- **URL:** https://github.com/vectordotdev/vrl/issues/7
- **Author:** @Djeezus
- **Status:** CLOSED (completed)
- **Created:** 2023-01-10T21:01:13Z
- **Closed:** 2023-04-11T16:48:01Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

"to_timestamp" does not recognize TIMESTAMP_ISO8601 pattern/format is.
"parse_grok" honors  [TIMESTAMP_ISO8601 pattern](https://github.com/daschl/grok/tree/master/patterns), but "to_timestamp" does not.

I would suggest to recognize the same pattern in both "to_timestamp" and "parse_grok"-patterns, so that a .timestamp can be matched and extracted from any field without the need to use parse_timestamp custom formats when the parse_grok did already match on an existing pattern.



### Attempted Solutions


In VRL tested:
```
$ . = { "@timestamp": "2023-01-10T05:05:05.55Z", "@metadata": { "beat": "filebeat", "type": "_doc", "version": "7.9.2" }, "host": { "name": "somehostname" }, "message": "2023-01-10 10:03:30.745 blah blah blah blah" }
{ "@metadata": { "beat": "filebeat", "type": "_doc", "version": "7.9.2" }, "@timestamp": "2023-01-10T05:05:05.55Z", "host": { "name": "somehostname" }, "message": "2023-01-10 10:03:30.745 blah blah blah blah" }

$ .flat = parse_grok!(.message, "^%{TIMESTAMP_ISO8601:datestamp} %{GREEDYDATA:logline}")
{ "datestamp": "2023-01-10 10:03:30.745", "logline": "blah blah blah blah" }

$ .timestamp = to_timestamp!(.flat.datestamp)
function call error for "to_timestamp" at (13:43): No matching timestamp format found for "2023-01-10 10:03:30.745"

$ .timestamp = to_timestamp!(.@timestamp)
t'2023-01-10T05:05:05.550Z'

### Proposal

_No response_

### References

#15802

### Version

v0.26.0
