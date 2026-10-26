# [#50] add `parse_envoy()` support?

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/50)
- **Status**: `OPEN`
- **Author**: [@parkedwards](https://github.com/parkedwards)
- **Created At**: `2022-06-23T01:32:51Z`
- **Updated At**: `2023-03-28T13:25:43Z`
- **Comments**: 2
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/50)

---

## Description

https://www.envoyproxy.io/docs/envoy/latest/configuration/observability/access_log/usage#default-format-string

^ envoy has a bunch of different logs, i know (and the ability to custom format them, which makes adding support on the Vector side...tricky)

but if there's appetite for it, I wrote a regex string for our Vector to parse our Envoy access logs (which are their request logs) -- they're similar to what you'd see in an apache format or nginx.  i imagine many envoy users are probably just using the default string format, and if so this parsing string might come in handy - and im sure you guys can do a much better job than i did.

https://regex101.com/r/pFQf5V/1
