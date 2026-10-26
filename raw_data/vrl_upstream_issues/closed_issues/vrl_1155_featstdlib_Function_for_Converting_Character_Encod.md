# Issue #1155: feat(stdlib): Function for Converting Character Encodings

- **URL:** https://github.com/vectordotdev/vrl/issues/1155
- **Author:** @powerumc
- **Status:** CLOSED (completed)
- **Created:** 2024-12-01T04:55:44Z
- **Closed:** 2024-12-10T15:54:28Z
- **Labels:** None

## Description

Our system utilizes both legacy systems and the latest Linux distributions. Occasionally, we encounter systems that operate with non-UTF-8 settings. When logs are sent via TCP from these systems, all Korean strings encoded in EUC-KR become corrupted.

To address this issue, I've created a functions.
The function signature is as follows.
```vrl
decode_charset(value, from_charset)
encode_charset(value, to_charset)
```

If this addition is beneficial for the VRL project, I would like to submit a pull request.
