# [#1692] Preserve numeric precision with `decimal` type

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1692)
- **Status**: `OPEN`
- **Author**: [@benjamin-awd](https://github.com/benjamin-awd)
- **Created At**: `2026-03-08T17:07:58Z`
- **Updated At**: `2026-06-01T14:19:46Z`
- **Comments**: 2
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1692)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

Today, VRL has no way to preserve full numeric precision, and silently corrupts data (i.e. causes precision loss) in several scenarios:
- `parse_json('{"val": 0.12379999458789825}')` → `0.12379999458789824` (#1503)
- `parse_json({"val": 9223372036854775808})` → `9223372036854776000` (#544)
- `9223372036854775807 / 1` → `9223372036854776000` (#254)
- `to_float(4052555153018976267)` → `4052555153018976256` ([vector#5530](https://github.com/vectordotdev/vector/issues/5530))

On the Vector side, this means that codecs like Avro must reject `Decimal`/`BigDecimal` values entirely on ingress. On egress, sinks using Arrow encoding (ClickHouse, Parquet, Zerobus etc) must upcast `float64` → `Decimal128`, which is not desirable since it introduces imprecision.

### Attempted Solutions

### 1. Enable serge-json's `arbitrary_precision` feature

This is the most obvious fix. However, enabling `arbitrary_precision` is global and not per-call. Enabling it changes how every `serde_json` deserialization works across the entire crate -- every number gets heap-allocated as a `String` which adds unnecessary overhead to cases where precision doesn't matter. There is no way to opt in per-source or per-call.

Making this opt-in (as per #1503) would require either adding an extra JSON crate like `sonic-rs` (which supports per-call arbitrary precision), or finding a way to import `serde_json` twice with different feature flags (I don't think this is possible to do with Cargo -- AFAIK a crate can only appear once in a dependency graph with a single set of features).

### 2. Strings as workaround

The current workaround is to use strings where possible.

This works for pure passthrough but:
- Loses the ability to compare values (e.g., filter events where `val > 100`)
- Downstream sinks expecting numeric JSON fields will reject strings -- `"19.99"` (string) is not `19.99` (number).
- Requires manual string conversion for every numeric field in VRL transforms
- Type checking becomes impossible — no way to distinguish "this is a precise number" from an arbitrary string

### 3. Integer scaling (multiply by 10^n)

Represent values as scaled integers (e.g., store `19.99` as `1999` with an implicit scale factor). Works for known-scale values but:
- Requires knowing the scale at parse time, which isn't always possible with heterogeneous JSON
- Doesn't help with the `serde_json` deserialization problem -- the precision is already lost before VRL code runs

### Proposal

Add `Decimal` as a new primitive type in VRL's type system which holds a `rust_decimal::Decimal` directly (96-bit coefficient, scale 0–28, range ±7.9×10²⁸)

Instead of enabling `arbitrary_precision` project-wide, we can instead deserialize via `serde_json::value::RawValue`, which preserves the original string representation per call site without global side effects.

So far I'm thinking something like this:
```coffee
# Decimal literals
precise = d'0.12379999458789825'

# Comparison with float
f = 0.1 + 0.2       # Float: 0.30000000000000004
d = d'0.1' + d'0.2'  # Decimal: 0.3 (exact)
```

Examples:
```coffee
# Float precision preserved
parse_json('{"val": 0.12379999458789825}', arbitrary_precision: true)
# => {"val": 0.12379999458789825}  (without: 0.12379999458789824)

# Large integers beyond i64 preserved
parse_json('{"val": 9223372036854775808}', arbitrary_precision: true)
# => {"val": 9223372036854775808}  (without: 9223372036854776000)

# Arithmetic works as expected
total = d'19.99' * 3  # => d'59.97' (exact)
```

Conversion rules:
- Integers that fit in i64 → Value::Integer
- Everything else (fractional, or too large for i64) → Value::Decimal

On the Vector side, we could then add something like this:
1. `JsonDeserializerOptions` gains a new field:
   ```rust
   pub preserve_decimal_precision: bool,
   ```

2. When `preserve_decimal_precision` is enabled, the codec parses JSON via `serde_json` with `RawValue`. We then hen converted to the appropriate VRL type via `Value::try_from()`.

3. Numbers are converted as follows:
   - Integers that fit in `i64` become `Value::Integer`
   - Decimal numbers become `Value::Decimal`

I have a working implementation of this that I'd be happy to put up as a PR if there's interest.

### References

Related:
- https://github.com/vectordotdev/vrl/pull/1656
- https://github.com/vectordotdev/vector/issues/24418
