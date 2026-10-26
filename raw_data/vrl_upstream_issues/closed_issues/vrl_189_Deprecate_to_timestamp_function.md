# Issue #189: Deprecate `to_timestamp` function

- **URL:** https://github.com/vectordotdev/vrl/issues/189
- **Author:** @jszwedko
- **Status:** CLOSED (completed)
- **Created:** 2023-04-11T16:47:26Z
- **Closed:** 2023-10-12T14:31:14Z
- **Labels:** vrl:stdlib

## Description

Deprecate and remove `to_timestamp` function.

Reasoning from https://github.com/vectordotdev/vrl/issues/7#issuecomment-1503761940

> After some discussion on the team, we think having the to_timestamp function have a list of "known formats" does more harm than good since there isn't a clear rule we can apply for what formats qualify to be included. Instead, we'd like to push users to use the parse_timestamp function where they supply the format. Additionally, the to_timestamp function has a parameter, units, for interpreting integer values that we also think is a bit odd and would be better served via a specialized from_unix_timestamp function.

Depends on https://github.com/vectordotdev/vrl/issues/188 being done first.
