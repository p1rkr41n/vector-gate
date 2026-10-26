# [#120] VRL parse function for hexstring to string

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/120)
- **Status**: `OPEN`
- **Author**: [@msrpub](https://github.com/msrpub)
- **Created At**: `2021-04-26T17:35:03Z`
- **Updated At**: `2023-03-28T14:19:18Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/120)

---

## Description

We have several usecases which would require decode of hexstring to string from logs.
After text extraction with grok, there would be a need to get an hexstring to string function (parse_hexToString)

Example below:
74 65 73 74 20 73 74 72 69 6e 67 -> test string
7465737420737472696e67 -> test string
