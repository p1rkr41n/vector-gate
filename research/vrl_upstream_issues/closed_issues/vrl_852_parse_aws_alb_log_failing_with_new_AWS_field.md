# Issue #852: parse_aws_alb_log failing with new AWS field

- **URL:** https://github.com/vectordotdev/vrl/issues/852
- **Author:** @Alex-Waring
- **Status:** CLOSED (completed)
- **Created:** 2024-05-22T11:59:23Z
- **Closed:** 2024-06-03T20:50:37Z
- **Labels:** vrl:stdlib

## Description

AWS have added a new Transaction ID field to their ALB logs, and have not announced this so it's not in their docs yet. However for those who are on the rollout plan, the `parse_aws_alb_log` function is failing:

```
Vector unable to parse alb log: function call error for "parse_aws_alb_log" at (18:45): Log should be fully consumed: " TID_XXXX"
```

The parse_aws_alb_log function should have added to it the ability to conditionally parse this entry, if that's possible, until AWS confirm the rollout is complete.

To workaround this I have added:

```
strip_tid, err = split(.message, " TID_")[0]
if err != null {
    .@error = true
    .@error_msg = "Vector unable to parse alb log: " + err
} else {
    structured, err = parse_aws_alb_log(strip_tid)
    if err != null {
        .@error = true
        .@error_msg = "Vector unable to parse alb log: " + err
    } else {
        . = merge(., structured)
    }
}
```
