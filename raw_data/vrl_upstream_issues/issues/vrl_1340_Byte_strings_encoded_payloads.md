# [#1340] Byte strings/encoded payloads

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1340)
- **Status**: `OPEN`
- **Author**: [@jimmystewpot](https://github.com/jimmystewpot)
- **Created At**: `2025-03-16T22:53:58Z`
- **Updated At**: `2025-04-07T17:17:13Z`
- **Comments**: 3
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1340)

---

## Description

Hello,

We currently have an observability pipeline using Go's `json.RawMessage` ([]byte) encoding on a stream coming in via a pub/sub queue. I was reading through the docs and couldn't find a clear answer regarding how this would or should be handled with vrl.

I am keen to better understand how this use case could be done; if this is not currently possible, we are happy to contribute a feature, but I wanted to make sure that we didn't overlook 'the right way' to do this in the context of vector/vrl.

Thanks in advance,

James.
