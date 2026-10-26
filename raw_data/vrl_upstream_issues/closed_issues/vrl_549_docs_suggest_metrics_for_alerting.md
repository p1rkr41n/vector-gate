# Issue #549: docs: suggest metrics for alerting

- **URL:** https://github.com/vectordotdev/vrl/issues/549
- **Author:** @djudd
- **Status:** CLOSED (completed)
- **Created:** 2023-11-10T18:40:08Z
- **Closed:** 2023-11-28T19:51:21Z
- **Labels:** None

## Description

This is very much a nice-to-have thing, but one thing that's missing from the generally very helpful https://vector.dev/docs/setup/going-to-prod/ is advice on what metrics are best for alerting. I think at least the metrics, if not the precise thresholds, might be relatively common between installations? My quick scan of metrics has me alerting on component errors, unintentional discards, or throttling, as well as suspiciously low volume on key sinks, but it'd be good to have pointers on what that might miss.
