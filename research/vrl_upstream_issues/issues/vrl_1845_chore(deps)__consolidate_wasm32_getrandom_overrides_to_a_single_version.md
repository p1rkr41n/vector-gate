# [#1845] chore(deps): consolidate wasm32 getrandom overrides to a single version

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1845)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2026-07-01T17:30:38Z`
- **Updated At**: `2026-07-01T17:30:54Z`
- **Comments**: 0
- **Labels**: `type:tech debt`, `domain:deps`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1845)

---

## Description

## Context

The `wasm32-unknown-unknown` target requires explicit opt-in for entropy sources. We currently carry **three separate wasm32 target overrides** in `Cargo.toml` because three different generations of RustCrypto crates each pin a different major version of [`getrandom`](https://crates.io/crates/getrandom):

```toml
[target.'cfg(target_arch = "wasm32")'.dependencies]
getrandom02 = { package = "getrandom", version = "0.2", features = ["js"] }
getrandom03 = { package = "getrandom", version = "0.3", features = ["wasm_js"] }
getrandom   = { package = "getrandom", version = "0.4", features = ["wasm_js"] }
```

Each version is forced by a different part of the dep graph — they are not interchangeable (getrandom uses strict semver, each major is a distinct crate to Cargo).

## Why each version exists

| getrandom | Forced by | Pull chain |
|---|---|---|
| **0.2** | [`aes-siv`](https://crates.io/crates/aes-siv) 0.7, [`crypto_secretbox`](https://crates.io/crates/crypto_secretbox) 0.1, [`ipcrypt-rs`](https://crates.io/crates/ipcrypt-rs) 0.9 | old RustCrypto stack: `aead 0.5` → `rand_core 0.6` → `getrandom 0.2` |
| **0.3** | [`rand`](https://crates.io/crates/rand) 0.9 (direct VRL dep) | `rand 0.9` → `rand_core 0.9` → `getrandom 0.3` |
| **0.4** | [`aes-gcm`](https://crates.io/crates/aes-gcm) 0.11, [`chacha20poly1305`](https://crates.io/crates/chacha20poly1305) 0.11, [`aes`](https://crates.io/crates/aes) 0.9 | new RustCrypto stack: `aead 0.6` → `crypto-common 0.2` → `getrandom 0.4` |

## What needs to happen to consolidate

### Eliminate getrandom 0.2

Requires migrating three crates from old RustCrypto (aead 0.5 / cipher 0.4 / aes 0.8) to new (aead 0.6 / cipher 0.5 / aes 0.9):

| Crate | Currently used | Required | Upstream status |
|---|---|---|---|
| [`aes-siv`](https://crates.io/crates/aes-siv) | 0.7.0 | ≥ 0.8 (aead 0.6) | [`0.8.0-rc.3`](https://crates.io/crates/aes-siv/0.8.0-rc.3) — pre-release ([RustCrypto/AEADs](https://github.com/RustCrypto/AEADs)) |
| [`crypto_secretbox`](https://crates.io/crates/crypto_secretbox) | 0.1.1 | ≥ 0.2 (aead 0.6) | [`0.2.0-pre.0`](https://crates.io/crates/crypto_secretbox/0.2.0-pre.0) — pre-release only |
| [`ipcrypt-rs`](https://crates.io/crates/ipcrypt-rs) | 0.9.4 (aes 0.8) | version using aes 0.9 | no release yet; upstream issue filed at [jedisct1/rust-ipcrypt2](https://github.com/jedisct1/rust-ipcrypt2) |

### Eliminate getrandom 0.3

Requires `rand` to release a version that depends on `getrandom 0.4`. [`rand`](https://crates.io/crates/rand) 0.9 is the current stable release; no 0.10 exists yet ([rust-random/rand](https://github.com/rust-random/rand)).

## Goal state

Once all blockers resolve, the section collapses to a single line:

```toml
[target.'cfg(target_arch = "wasm32")'.dependencies]
getrandom = { package = "getrandom", version = "0.4", features = ["wasm_js"] }
```

This is a pure upstream dependency problem. No action is required in this repo until the upstream crates ship stable releases. This issue exists to track that work.
