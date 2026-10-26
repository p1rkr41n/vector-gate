# Issue #1100: Support for AES-SIV (RFC 5297) to provide Deterministic Encryption/Decryption

- **URL:** https://github.com/vectordotdev/vrl/issues/1100
- **Author:** @beardface
- **Status:** CLOSED (completed)
- **Created:** 2024-10-29T14:57:21Z
- **Closed:** 2024-10-30T15:41:31Z
- **Labels:** vrl:stdlib

## Description

## Details
We require Deterministic decryption for our use case, and the ideal algorithm for us is AES-SIV ([RFC 5297](https://datatracker.ietf.org/doc/html/rfc5297)).

More about why AES-SIV -> https://connect2id.com/blog/deterministic-encryption-with-aes-siv

## What needs to update?
The Decrypt lib will need to be updated to support AES-SIV ([here](https://github.com/vectordotdev/vrl/blob/main/src/stdlib/decrypt.rs)).

The following rust library provides an implementation for aes_siv encryption and decryption: https://docs.rs/aes-siv/latest/aes_siv/
