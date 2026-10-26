# [#1859] Release tool: checkpointing to resume a failed publish

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1859)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2026-07-13T13:42:07Z`
- **Updated At**: `2026-07-13T13:43:14Z`
- **Comments**: 0
- **Labels**: `domain:releasing`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1859)

---

## Description

## Context

Pre-flight checks ([#1858](https://github.com/vectordotdev/vrl/pull/1858)) make an aborted release run *unlikely*, but not impossible. `cargo publish` can still fail *after* the version bump and changelog commits are made:

- Transient registry outage or network hiccup.
- Verify-build failure on a downstream platform.
- Any post-commit step (tag, push, PR) that fails partway.

Today, recovering means finishing the remaining steps by hand (as happened with 0.34.0 — see [#1857](https://github.com/vectordotdev/vrl/pull/1857)).

## Proposal

Add checkpointing so a partial run can be resumed instead of unwound.

- Persist state to a scratch file (e.g. `.release-state.json`, git-ignored) after each successful step: branch created, version bumped, changelog committed, published, tagged, pushed, PR opened.
- On startup, if a checkpoint exists for the target version, offer to resume from the last completed step rather than starting over.
- Clear the checkpoint on successful completion.

## Outcome

We can resume releasing wherever the previous run left off. "Aborted release" stops being a manual recovery exercise.
