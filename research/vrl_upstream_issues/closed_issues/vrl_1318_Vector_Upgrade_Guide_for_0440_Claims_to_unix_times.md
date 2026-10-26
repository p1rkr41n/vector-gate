# Issue #1318: Vector Upgrade Guide for 0.44.0 Claims to_unix_timestamp can return an error

- **URL:** https://github.com/vectordotdev/vrl/issues/1318
- **Author:** @mohammed-uddin
- **Status:** CLOSED (completed)
- **Created:** 2025-03-04T20:22:46Z
- **Closed:** 2025-03-04T22:06:43Z
- **Labels:** vrl:compiler, vrl:stdlib

## Description

Hi,

I'm upgrading from vector 0.43.1-debian to 0.45.0-debian.

The 0.44.0 Upgrade guide says the following

![Image](https://github.com/user-attachments/assets/d3da052a-7c05-411a-974e-15923473b961)

due to https://github.com/vectordotdev/vrl/pull/979

Is that actually true tho? I have added error handling code and found that it is not needed.

[Here's what the vector playground says](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLnRpbWVzdGFtcCwgZXJyID0gdG9fdW5peF90aW1lc3RhbXAodCcyMDIxLTAxLTAxVDAwOjAwOjAwKzAwOjAwJywgdW5pdDogXCJuYW5vc2Vjb25kc1wiKVxuIiwiZXZlbnQiOnsibWVzc2FnZSI6IkhlbGxvIFZSTCIsImZvbyI6ImRlbGV0ZSBtZSIsImh0dHBfc3RhdHVzIjoiMjAwIn0sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9) with VRL version 0.22.0

![Image](https://github.com/user-attachments/assets/ffa913dc-b635-41f6-9294-69ba697404c8)

Have I misread your upgrade guide?

The latest docs still say the function is infallible: https://vector.dev/docs/reference/vrl/functions/#to_unix_timestamp

