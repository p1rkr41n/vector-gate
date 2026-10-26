# [#1429] Allow override grok patterns via aliases in `parse_groks` function

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1429)
- **Status**: `OPEN`
- **Author**: [@piotrminkina](https://github.com/piotrminkina)
- **Created At**: `2025-06-23T13:15:03Z`
- **Updated At**: `2026-06-16T13:09:26Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`, `stdlib:parse_groks`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1429)

---

## Description

Hello,

Please consider this file with grok patterns that are officially used in Vector: https://github.com/mmastrac/grok/blob/main/patterns/haproxy.pattern

As you can see, this file contains the patterns `HAPROXYCAPTUREDREQUESTHEADERS` and `HAPROXYCAPTUREDRESPONSEHEADERS`, which are dedicated to customization because they depend on which HTTP request and response headers will be captured by HAProxy and added to the access log.
I expect that the `parse_groks` function in the `aliases` or `alias_sources` key will allow me to override these names and substitute my own pattern that matches my HAProxy configuration. I assume that the Vector configuration should look like this:

```yaml
sources:
  haproxy_logs:
    type: file
    include:
      - /var/log/haproxy.log
    read_from: beginning

transforms:
  parse_haproxy:
    type: remap
    inputs:
      - haproxy_logs
    drop_on_error: false
    source: |
      . |= parse_groks!(
        .message,
        patterns: [ "%{HAPROXYHTTP}" ],
        aliases: {
          "HAPROXYCAPTUREDREQUESTHEADERS": "%{DATA:request_header_host_short}\\.%{HOSTNAME:request_header_host_domain}\\|%{DATA:request_header_x_forwarded_for}"
        }
      )
      del(.message)
```

Unfortunately, it seems that this is not working because the old pattern for `HAPROXYCAPTUREDREQUESTHEADERS` is still being used. So I still see the `captured_request_headers` key in the output instead of `request_header_host_short`, `request_header_host_domain`, and `request_header_x_forwarded_for` as per my alias configuration.

For an application like _fstab/grok_exporter_, this works fine. I simply add the _haproxy.override_ file (this is my convention) to the _patterns_ directory, where I have defined my own pattern with the same name, and after restarting the application, I immediately see the desired effect. It would be very nice if similar behavior were also implemented in Vector.

Regards
Piotr Minkina

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

_No response_

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

vectordotdev/vector#9660

### Version

0.47.0
