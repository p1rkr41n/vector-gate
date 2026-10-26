# Issue #1312: encoding_rs marked as optional=false

- **URL:** https://github.com/vectordotdev/vrl/issues/1312
- **Author:** @PSeitz
- **Status:** CLOSED (completed)
- **Created:** 2025-03-03T11:19:01Z
- **Closed:** 2025-03-05T13:52:25Z
- **Labels:** None

## Description

`encoding_rs` in Cargo.toml is in the optional dependencies list, but it is `optional = false`. Not sure if this is a typo.  
Side note: I ran into a compile issue, where the selected version conflicts with another in my project

It was added in this PR: https://github.com/vectordotdev/vrl/commit/ddcb49efc6d938e07decc882c77c64936803c711

@powerumc @jszwedko 
