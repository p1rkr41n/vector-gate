# [#112] Expand supported redactors for redact

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/112)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2021-05-13T16:01:20Z`
- **Updated At**: `2023-03-28T14:16:24Z`
- **Comments**: 6
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/112)

---

## Description

Broken off from https://github.com/timberio/vector/pull/7250#discussion_r631912508

The initial implementation of `redact` just had one redactor that always replaced with `[REDACTED]`. We should expand this to support additional redactors like:

* Customizing the redaction string
* Hashing the value to have consistent replacement text
* Masking such as only showing the last 4 for social security numbers
