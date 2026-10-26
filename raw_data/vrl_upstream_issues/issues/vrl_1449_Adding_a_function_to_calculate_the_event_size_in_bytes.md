# [#1449] Adding a function to calculate the event size in bytes

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1449)
- **Status**: `OPEN`
- **Author**: [@omers](https://github.com/omers)
- **Created At**: `2025-07-16T07:12:21Z`
- **Updated At**: `2026-06-01T14:19:33Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1449)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

- Calculate the total amount of events in Gb / Tb per day per service
- Add anomaly alerts on High volume ingestion per hour / day etc.
- Generate cost reports based on the total amount of data per team / service / customer etc.

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

Today we do it with logstash as:

```ruby
  ruby {
    code => '
      event.set("log_size_bytes", event.to_hash.to_s.bytesize)
    '
  }
```
