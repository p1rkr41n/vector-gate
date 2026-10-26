# [#147] add `credit_card` filter to `redact` function

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/147)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2020-11-25T14:30:11Z`
- **Updated At**: `2026-06-16T13:11:48Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:redact`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/147)

---

## Description

After vectordotdev/vector#5221 lands, we want to expand the list of filters to make it easy to filter sensitive data without having to write your own regexp (and to make sure those implementations are as performant as possible).

First on the list is a credit card filter:

```json
{ "message": "order paid using credit card number 5555 5555 5555 4444" }
```

```rust
.message = redact(.message, filters = ["credit_card"])
```

```json
{ "message": "order paid using credit card number ****" }
```

Some relevant references:

* http://www.richardsramblings.com/2012/12/the-perfect-credit-card-number-regex/
* https://github.com/solvvy/redact-pii/blob/3a3f076a7a375fd629bab0e25b084cf154b1445f/src/built-ins/simple-regexp-patterns.ts
* https://github.com/microsoft/presidio/blob/7935adf03c80a0ba5d53c6affb7d7c78198affaa/presidio-analyzer/presidio_analyzer/predefined_recognizers/credit_card_recognizer.py
* https://github.com/luhnmod10/rust
* https://github.com/valeriansaliou/rs-card-validate

ref vectordotdev/vector#4519
