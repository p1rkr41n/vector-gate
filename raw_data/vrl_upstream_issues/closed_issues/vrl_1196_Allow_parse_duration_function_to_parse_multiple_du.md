# Issue #1196: Allow `parse_duration` function to parse multiple duration similar to Golang's `time.ParseDuration`

- **URL:** https://github.com/vectordotdev/vrl/issues/1196
- **Author:** @titaneric
- **Status:** CLOSED (completed)
- **Created:** 2024-12-27T18:36:11Z
- **Closed:** 2025-01-03T19:55:31Z
- **Labels:** vrl:stdlib

## Description

Hi, I would like to add the feature for VRL, which is allow `parse_duration` function to parse give string with multiple units such as `1h1s`, and `3s3ms` and so on similar to golang's [time.ParseDuration](https://cs.opensource.google/go/go/+/refs/tags/go1.23.4:src/time/format.go;l=1617).

Basically, golang's implementation parse given string until finding the duration unit, and keeps finding next digit unit match next duration unit. So, space is not allowed in the given duration string in golang. But since space is already allowed in VRL's `parse_duraiton`. I think space could be added for multiple-units duration string.
However, golang's implementation allows sign for given duration string. Whether we should add the support for signed duration deserves another issue opened.
