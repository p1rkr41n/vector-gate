# Issue #298: Support both Big and Little Endian for `AES-*-CTR` encryption modes

- **URL:** https://github.com/vectordotdev/vrl/issues/298
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2023-07-05T18:15:56Z
- **Closed:** 2023-07-10T13:48:42Z
- **Labels:** None

## Description

VRL currently hard-codes this to little endian. It would be nice to support both since it appears that Java uses big endian.
This can probably be added by adding `AES-*-CTR-BE`, `AES-*-CTR-LE` and deprecating `AES-*-CTR`. We should probably check how other software normally handles this too though.
