# [#101] Keep `lib/stdlib/data/user_agent_regexes.yaml` up to date

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/101)
- **Status**: `OPEN`
- **Author**: [@ktff](https://github.com/ktff)
- **Created At**: `2021-08-02T16:20:40Z`
- **Updated At**: `2023-03-28T14:01:27Z`
- **Comments**: 3
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/101)

---

## Description

File `lib/vrl/stdlib/data/user_agent_regexes.yaml` with regexes for parsing user agent string was introduced in vectordotdev/vector#8262. It's a copy of  https://github.com/ua-parser/uap-core/blob/master/regexes.yaml file so it needs to be kept up to date. 

The original file is updated on average once a month so it would be nice to also update then but we can be more coarse than that. The best option would be to automize this. The second best option would be to add some notification script which would detect changes and open an issue for it.

