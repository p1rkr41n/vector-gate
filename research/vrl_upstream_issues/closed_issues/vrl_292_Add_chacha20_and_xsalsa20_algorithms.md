# Issue #292: Add `chacha20` and `xsalsa20` algorithms

- **URL:** https://github.com/vectordotdev/vrl/issues/292
- **Author:** @alisa101rs
- **Status:** CLOSED (completed)
- **Created:** 2023-07-05T07:13:03Z
- **Closed:** 2023-07-14T13:29:31Z
- **Labels:** None

## Description

# Problem 

Currently, vector supports only AES-* encryption and decryption algorithms.

# Proposal

Add support for [chacha20, xchacha20](https://docs.rs/chacha20poly1305/latest/chacha20poly1305/) and [xsalsa20](https://docs.rs/crypto_secretbox/latest/crypto_secretbox/#) algorithms.
