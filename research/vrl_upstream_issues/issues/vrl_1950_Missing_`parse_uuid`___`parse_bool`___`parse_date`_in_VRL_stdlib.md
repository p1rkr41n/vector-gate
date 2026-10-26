# [#1950] Missing `parse_uuid` / `parse_bool` / `parse_date` in VRL stdlib

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1950)
- **Status**: `OPEN`
- **Author**: [@28515graj](https://github.com/28515graj)
- **Created At**: `2026-09-15T19:43:53Z`
- **Updated At**: `2026-09-17T18:11:52Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1950)

---

## Description


**Vector version:** 0.58.0 (VRL 0.35.0)

**Severity:** Minor (workarounds available)

**Description:**

VRL stdlib has `to_int`, `to_bool`, `to_timestamp`, but lacks strict parsers. The `uuid` crate is already a VRL dependency (used by `uuid_v4`, `uuid_v7`, `uuid_from_friendly_id`), so adding `parse_uuid` would be trivial.

**Reproduction:**

```vrl
# Try parsing a UUID string:
.uuid_string = "550e8400-e29b-41d4-a716-446655440000"
.parsed, err = parse_uuid(.uuid_string)
# Result: error[E105]: call to undefined function
```

`parse_bool`:
```vrl
.r1 = parse_bool("yes")
# Result: error[E105]: call to undefined function
```

`parse_date`:
```vrl
.r2 = parse_date("2026-09-15")
# Result: error[E105]: call to undefined function
```

**Confirmed in source:** the VRL stdlib directory `vrl/src/stdlib/` has files like `parse_int.rs`, `parse_float.rs`, `parse_csv.rs`, `parse_regex.rs`, `parse_json.rs`, `parse_timestamp.rs`, but no `parse_uuid.rs`, `parse_bool.rs`, or `parse_date.rs`.

**Use cases requiring these:**

1. Validating incoming UUID strings before inserting into a CH `UUID` column (currently requires regex workaround).

2. Strict boolean coercion without surprising accepts (`to_bool("yes")` returns true, which surprises users).

3. Date-only columns in CH: currently must append `00:00:00` and parse as timestamp.

**Suggested additions:**

Add `parse_uuid(value: string) -> UUID` (uses `uuid::Uuid::parse_str`).
Add `parse_bool_strict(value: string) -> bool` accepting only `"true"/"false"/"1"/"0"`.
Add `parse_date(value: string, format: string) -> Date` returning `Timestamp` at 00:00:00 UTC.

**Workaround examples:**

```vrl
# UUID validation regex (ugly but works)
uuid_str = "550e8400-e29b-41d4-a716-446655440000"
if !match(uuid_str, r'^[0-9a-fA-F]{8}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{4}-[0-9a-fA-F]{12}$') {
  abort "col_uuid invalid"
}

# Date workaround
ts, err = parse_timestamp(date + " 00:00:00", format: "%Y-%m-%d %H:%M:%S")
```

**Impact:** Forces users to write regex parsers for UUID validation and requires date-only columns to be mocked as timestamps.
