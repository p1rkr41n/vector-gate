# Issue #6897: Respect Vector's default timezone config in VRL

- **URL:** https://github.com/vectordotdev/vector/issues/6897
- **Author:** @JeanMertz
- **Status:** CLOSED (completed)
- **Created:** 2021-03-26T12:02:17Z
- **Closed:** 2021-07-09T19:48:44Z
- **Labels:** domain:vrl

## Description

Default (local and global) time zone configurations were added in https://github.com/timberio/vector/pull/6533, with this notable comment:

> Notably absent from the list of transforms is `remap`, which currently always uses the system local time zone. I propose we defer support for configuring this in remap to a separate issue.

I couldn't find this issue (cc @bruceg, my GitHub search-fu might just be lacking), but this was recently asked on Discord, so I figured I'd file this for tracking.

On solving this:

We should do the following steps:

1. Add the time zone config to Vector's `remap` transform.
2. Add the defined time zone to `vrl::Context`.
3. Allow passing in a custom time zone to `Runtime::resolve`.
4. Update time-zone related expressions/functions to take this new piece of context into account.
5. Add tests to validate all of this works as expected.
