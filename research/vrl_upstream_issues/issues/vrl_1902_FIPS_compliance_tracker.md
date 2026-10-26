# [#1902] FIPS compliance tracker

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1902)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2026-08-25T13:09:36Z`
- **Updated At**: `2026-08-25T13:13:53Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1902)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->

### Use Cases

Projects embedding VRL need to produce artifacts whose cryptographic operations are provided exclusively by an approved FIPS-validated module operating in its approved mode. Vector is one such consumer and is tracking an official FIPS-compliant build in vectordotdev/vector#8435.

VRL's full `stdlib` currently enables both `enable_crypto_functions` and `enable_network_functions`. The crypto functions use several pure-Rust implementations for encryption, hashing, and MACs, while network functions currently use a `reqwest`/Rustls path that can select `ring`. Those implementations are not validated as part of the cryptographic module expected to provide FIPS-approved services for the consuming application.

This issue is intended as the catch-all tracker for defining and implementing VRL's role in FIPS-compatible downstream builds.

### Proposal

Define and support a VRL compilation feature suitable for downstream FIPS builds. 

- [ ] Starting point: provide a supported restricted build profile that excludes crypto and network implementations that are not FIPS compliant.
- [ ] Make the TLS/crypto provider used by network functions configurable so downstream builds can select an approved provider.
- [ ] Add validation that prevents dependencies such as `ring` or standalone crypto implementations from entering the restricted/FIPS feature graph unexpectedly.
- [ ] Label functions as FIPS compliant (or not).
- [ ] Coordinate the resulting feature set with Vector's FIPS build and release validation.

### References

* vectordotdev/vector#8435
* vectordotdev/vector#16535
* https://github.com/rustls/rustls/issues/521

