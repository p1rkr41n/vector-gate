# [#1636] Support AES-GCM in `encrypt`/`decrypt` functions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1636)
- **Status**: `OPEN`
- **Author**: [@dodo0822](https://github.com/dodo0822)
- **Created At**: `2026-02-12T19:00:24Z`
- **Updated At**: `2026-06-16T13:09:18Z`
- **Comments**: 0
- **Labels**: `stdlib:decrypt`, `stdlib:encrypt`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1636)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

Encryption/decryption using AES-GCM.

### Attempted Solutions

Currently the encrypt/decrypt functions in VRL support various AES modes such as CTR and CBC, but GCM is missing.

### Proposal

The [aes_gcm](https://crates.io/crates/aes-gcm) crate provides GCM implementation and has a similar interface to the existing AES modes. It should be a small effort to add new modes to the VRL functions and connect it with `aes_gcm`. I will send out a PR but keeping this discussion open for any feedback!

### References

_No response_
