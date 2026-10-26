# Issue #602: Add a safe mode that disable functions who have access to more than event data

- **URL:** https://github.com/vectordotdev/vrl/issues/602
- **Author:** @pront
- **Status:** CLOSED (completed)
- **Created:** 2023-12-19T15:40:54Z
- **Closed:** 2026-02-26T18:47:07Z
- **Labels:** None

## Description

Related to https://github.com/vectordotdev/vrl/issues/348.

Functions such as `get_env_var` and `get_hostname` should be disabled in safe mode.
