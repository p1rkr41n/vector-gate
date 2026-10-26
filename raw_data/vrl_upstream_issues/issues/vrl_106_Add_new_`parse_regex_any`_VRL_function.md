# [#106] Add new `parse_regex_any` VRL function

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/106)
- **Status**: `OPEN`
- **Author**: [@rabbitstack](https://github.com/rabbitstack)
- **Created At**: `2021-07-02T12:55:54Z`
- **Updated At**: `2023-03-28T14:12:39Z`
- **Comments**: 3
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/106)

---

## Description

As discussed in Discord with Jean Mertz, it would be very valuable to provide a VRL function for regex parsing that can accept a list of regex patterns, similar to how the deprecated regex parser operates.

From Discord:

>Unfortunately there's no solution to this right now. We did add a match_any (https://vector.dev/docs/reference/vrl/functions/#match_any) function to speed up matching cases, but we don't have a parse_regex_any yet.

> We are tracking compile-time optimisations in https://github.com/timberio/vector/issues/7636, which would include cases like these, but there's nothing concrete yet.

> In the mean time, feel free to open an issue for this specific use-case, as I don't see a reason not to add parse_regex_any to at least have a solution in place until we have those optimisations.

