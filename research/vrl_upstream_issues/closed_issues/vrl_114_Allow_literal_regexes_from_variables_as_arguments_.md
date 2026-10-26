# Issue #114: Allow literal regexes from variables as arguments to VRL functions

- **URL:** https://github.com/vectordotdev/vrl/issues/114
- **Author:** @jszwedko
- **Status:** CLOSED (completed)
- **Created:** 2021-05-12T15:21:15Z
- **Closed:** 2023-07-07T19:54:49Z
- **Labels:** type:enhancement, vrl:stdlib

## Description

A user ran into an issue trying to assign a regex to a variable in VRL and then use that variable in `parse_regex`. This fails because we currently require regex literals but this could be relaxed to allow a variable that contains a regex.

That is, this program should work:

```
my_regex = r'(?<Pfoo>e)'
parse_regex("test", my_regex)
```

