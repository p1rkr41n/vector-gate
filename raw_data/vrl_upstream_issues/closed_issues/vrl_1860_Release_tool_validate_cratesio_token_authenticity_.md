# Issue #1860: Release tool: validate crates.io token authenticity (or restructure flow so we don't need to)

- **URL:** https://github.com/vectordotdev/vrl/issues/1860
- **Author:** @pront
- **Status:** CLOSED (completed)
- **Created:** 2026-07-13T14:07:09Z
- **Closed:** 2026-07-13T14:10:47Z
- **Labels:** domain:releasing

## Description

## Context

Pre-flight in #1858 was originally supposed to validate that the configured crates.io token is valid before mutating anything. Two attempts didn't work:

1. `cargo owner --list vrl` — unauthenticated on crates.io (`GET /api/v1/crates/{name}/owners` runs `list_owners` with no auth check).
2. `GET /api/v1/me` — uses `AuthCheck::only_cookie()` and rejects API-token auth outright.

A search of the crates.io controllers (`rust-lang/crates.io`) found no non-mutating endpoint that accepts an API token: every `AuthCheck::default()` route is either a mutation (`POST /api/v1/crates/new` publish, `PUT/DELETE /api/v1/crates/{name}/owners`, `POST /api/v1/me/tokens` create) or a destructive delete (`DELETE /api/v1/tokens/current` revokes the token you just used to authenticate).

So today's pre-flight is a presence check only — it catches "never ran `cargo login`" (the failure mode from the 0.34.0 release) but not "token expired" or "token has wrong scope". Those still surface at `cargo publish` after the version bump and changelog commits are made.

## Options

### A. Ugly-but-benign probe

`POST /api/v1/me/tokens` runs `AuthCheck::default()` first, then rejects API-token callers with 400 ("cannot use an API token to create a new API token"). No side effects. This means:
- Valid token → 400 with that specific body
- Invalid token → 401
- Would need to send a placeholder request body

Downsides: relies on internal ordering of checks; fragile if crates.io reorganizes.

### B. Restructure flow so a failed publish leaves no state

If `cargo publish` runs before the release commits, or if the commits auto-rollback on publish failure, the whole "did they run `cargo login`" check becomes moot. Sketch:

1. Bump `Cargo.toml` (in-tree, uncommitted).
2. `cargo publish --allow-dirty` — this is what actually validates auth.
3. If publish succeeded: commit version, generate changelog, commit, tag, push, PR.
4. If publish failed: `git checkout -- Cargo.toml Cargo.lock` and exit.

Also solves the checkpointing problem from #1859 for this specific failure.

### C. Live with the presence check

Document the limitation and accept that expired/wrong-scope tokens fail at `cargo publish`. Combined with #1859 (resume-from-checkpoint), the manual recovery cost is much lower.

## Recommendation

B is the cleanest — it removes an entire class of failure rather than trying to detect it. C is the do-nothing fallback if B turns out to be more disruptive than expected.
