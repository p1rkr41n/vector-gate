# Issue #491: Support microseconds in from_unix_timestamp

- **URL:** https://github.com/vectordotdev/vrl/issues/491
- **Author:** @emikitas
- **Status:** CLOSED (completed)
- **Created:** 2023-10-03T14:33:39Z
- **Closed:** 2023-10-05T13:52:54Z
- **Labels:** None

## Description

Hi,

As of version 0.4.31, chrono has a function that takes a UNIX timestamps in microseconds and returns a DateTime struct: [Utc.timestamp_micros](https://docs.rs/chrono/latest/chrono/offset/trait.TimeZone.html#method.timestamp_micros).
I want to add support for using UNIX microsecond timestamps in `from_unix_timestamp.rs`. I forked the repository and implemented my request [here](https://github.com/vectordotdev/vrl/compare/main...final-israel:vrl:support_microseconds_in_from_unix_timestamp).

With this, would vector users be able to use the new `Unit::Microseconds` in their vrl remaps?
Is my implementation acceptable?
