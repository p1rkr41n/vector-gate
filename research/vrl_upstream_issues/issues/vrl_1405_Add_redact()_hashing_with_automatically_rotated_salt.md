# [#1405] Add redact() hashing with automatically rotated salt

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1405)
- **Status**: `OPEN`
- **Author**: [@nemobis](https://github.com/nemobis)
- **Created At**: `2025-05-21T07:32:44Z`
- **Updated At**: `2026-06-16T13:09:28Z`
- **Comments**: 0
- **Labels**: `stdlib:redact`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1405)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

In order to reduce [personal data](https://commission.europa.eu/law/law-topic/data-protection/data-protection-explained_en) stored in our logs, I want to be able to hash identifiers such as IP addresses in a way that makes deanonymization difficult or impossible.

### Attempted Solutions

I've successfully used the [redact](https://vector.dev/docs/reference/vrl/functions/#redact) function to completely remove personal data and to hash non-personal data. However, sometimes it's useful to know whether a specific IP address is dominating access logs, or similar patterns. Hashing the IP address allows to notice such repetition, but it defeats the purpose of redaction because the hash can be reversed.

### Proposal

Similar to [EFF's cryptolog](https://github.com/EFForg/cryptolog), add a hashing option similar to `sha2` but with a pseudorandomly generated salt changed automatically every `x` (configurable) days. From their explanation:

> Technically, cryptolog takes 16 bytes of random data from /dev/urandom and stores it in a file (called the salt). It then calculates a sha256 hash of the salt concatonated with the original IP address, base64-encodes that, and chops off the first six characters of the result. That's what gets stored instead of the IP address in the resulting log entry. Of course this means that if someone who wishes to know the original IP addresses gets access to these logs, all they need to know is the salt (which is also stored on the hard drive) to uncover the original IPs. In order to prevent this, the salt gets updated once a day with a new random 16 bytes. At worst, an attacker can only get the last day's worth of original IP addresses.

The Internet Archive is an example of a large webserver which successfully uses cryptolog.

An initial implementation does not need to care about keeping the salt consistent across different instances in a fleet, but it might allow to provide the salt via configuration. It would then be possible to roll your own way to generate and distribute the salt.

### References

_No response_

### Version

_No response_
