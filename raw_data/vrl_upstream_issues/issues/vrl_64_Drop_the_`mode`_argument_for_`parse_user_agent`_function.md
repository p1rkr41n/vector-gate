# [#64] Drop the `mode` argument for `parse_user_agent` function

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/64)
- **Status**: `OPEN`
- **Author**: [@binarylogic](https://github.com/binarylogic)
- **Created At**: `2022-05-11T21:38:59Z`
- **Updated At**: `2026-06-16T13:11:04Z`
- **Comments**: 4
- **Labels**: `vrl:stdlib`, `stdlib:parse_user_agent`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/64)

---

## Description

After reviewing https://github.com/vectordotdev/vector/pull/12704/files, we should consider dropping the `mode` argument for the `parse_user_agent` function. This argument is unclear. It's not clear what's being traded off with the different modes. I also, generally, find `fast` to be a strange option as well, because who doesn't want fast?

If possible, I'd rather the argument reflect the output, where users can turn on enriched attributes one-by-one as needed.
