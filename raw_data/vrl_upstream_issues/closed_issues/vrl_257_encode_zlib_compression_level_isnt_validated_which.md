# Issue #257: `encode_zlib` `compression_level` isn't validated which can lead to a panic

- **URL:** https://github.com/vectordotdev/vrl/issues/257
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2023-05-25T02:39:56Z
- **Closed:** 2023-08-17T19:04:13Z
- **Labels:** vrl:stdlib, fuzz

## Description

Using a compression level higher than 10 will trigger a panic in the `encode_zlib` function. This should be checked by VRL and return an error instead. This will require the function to be fallible (unless the `compression_level` is a valid constant value)

Example
```coffee
encode_zlib("d",66)
```
```sh
thread 'main' panicked at 'assertion failed: level.level() <= 10', /home/nathan/.cargo/registry/src/github.com-1ecc6299db9ec823/flate2-1.0.26/src/ffi/rust.rs:129:9
```

VRL version `main` (`1ff642dc940c7d07`)
