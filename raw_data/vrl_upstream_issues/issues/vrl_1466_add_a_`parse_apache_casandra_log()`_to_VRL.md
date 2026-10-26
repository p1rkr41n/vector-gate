# [#1466] add a `parse_apache_casandra_log()` to VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1466)
- **Status**: `OPEN`
- **Author**: [@kquinsland01](https://github.com/kquinsland01)
- **Created At**: `2025-08-05T18:47:48Z`
- **Updated At**: `2026-06-01T14:19:36Z`
- **Comments**: 0
- **Labels**: `new function`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1466)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

The [docs for `parse_regex()`](https://vector.dev/docs/reference/vrl/functions/#parse_regex) has this call-out:

> VRL aims to provide purpose-specific [parsing functions](https://vector.dev/docs/reference/vrl/functions/#parse-functions) for common log formats. Before reaching for the parse_regex function, see if a VRL [parse_* function](https://vector.dev/docs/reference/vrl/functions/#parse-functions) already exists for your format. If not, we recommend [opening an issue](https://github.com/vectordotdev/vector/issues/new?labels=type%3A+new+feature) to request support for the desired format.

So that's what i'm doing with this ticket.


For reference, apache cassandra has a default `logback` config:

```xml

<!-- ... -->
    <encoder>
      <pattern>%-5level [%thread] %date{ISO8601} %F:%L - %msg%n</pattern>
    </encoder>
<!-- ... -->
```

Which emits logs like this:

```log
INFO  [ScheduledTasks:1] 2025-08-05 18:27:04,016 TokenMetadata.java:527 - Updating topology for all endpoints that have changed
INFO  [StorageServiceShutdownHook] 2025-08-05 18:27:15,792 HintsService.java:210 - Paused hints dispatch
INFO  [StorageServiceShutdownHook] 2025-08-05 18:27:15,795 Server.java:179 - Stop listening for CQL clients
INFO  [StorageServiceShutdownHook] 2025-08-05 18:27:15,795 Gossiper.java:1720 - Announcing shutdown
```

Which can be parsed with this regex:

```vrl
matches, err = parse_regex(.message, r'^(?P<level>\w+)\s+\[(?P<thread>[^\]]+)\]\s+(?P<ts>\d{4}-\d{2}-\d{2} \d{2}:\d{2}:\d{2},\d{3})\s+(?P<file>\S+):(?P<line>\d+)\s+-\s+(?P<msg>.+)$')
```

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

_No response_

### Version

vector 0.47.0 (aarch64-unknown-linux-musl 3d5af22 2025-05-20 13:53:41.638057046)
