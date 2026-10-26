# [#1824] datadog_filter: wildcard_regex fails to match strings with trailing newline

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1824)
- **Status**: `OPEN`
- **Author**: [@gwenaskell](https://github.com/gwenaskell)
- **Created At**: `2026-06-17T11:59:44Z`
- **Updated At**: `2026-07-08T19:40:16Z`
- **Comments**: 1
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1824)

---

## Description

## Bug Description

`wildcard_regex` in `src/datadog/filter/regex.rs` produces patterns of the form `^.*$`. This fails to match field values that end with a newline character (`\n`), even when the pattern should logically match the entire string.

## Root Cause

```rust
// src/datadog/filter/regex.rs
pub fn wildcard_regex(to_match: &str) -> Regex {
    Regex::new(&format!(
        "^{}$",
        regex::escape(to_match).replace("\\*", ".*")
    ))
    .expect("invalid wildcard regex")
}
```

Two interactions combine to cause the failure:

1. **`.` does not match `\n` by default** in Rust's `regex` crate — so `.*` stops before the trailing newline.
2. **`$` anchors to the absolute end of the string** (after the `\n`), not just before the final newline.

This leaves a gap: `.*` cannot advance past the `\n`, and `$` cannot be reached without crossing it. The match fails.

## Affected Queries

Any Datadog Search Syntax query that goes through the `wildcard` branch of `EventFilter` for `Field::Attribute` or `Field::Reserved` is affected. Concretely, for a field value `"some content\n"`:

| Query pattern | Parsed as | Matching function | Result |
|---|---|---|---|
| `field:*` | `AttributeWildcard("*")` | `wildcard_regex("*")` = `^.*$` | ❌ fails |
| `field:*some*` | `AttributeWildcard("*some*")` | `wildcard_regex("*some")` = `^.*some.*$` | ❌ fails |
| `field:*some` | `AttributeWildcard("*some")` | `wildcard_regex("*some")` = `^.*some$` | ❌ fails |
| `field:some*` | `AttributePrefix("some")` | `value.starts_with("some")` | ✅ works |

Note that `AttributePrefix` (trailing-`*`-only patterns) is **not** affected because it uses `starts_with()` instead of a regex.

`word_regex` (used for `Field::Default`) is also not affected because `\b.*\b` does not use `^...$` anchors.

## Reproducer

```rust
use vrl::datadog_filter::regex::wildcard_regex;

let value = "hello world\n"; // trailing newline
let re = wildcard_regex("*");  // produces ^.*$

assert!(re.is_match(value));  // FAILS — returns false
assert!(re.is_match(value.trim_end_matches('\n')));  // passes
```

## Proposed Fix

Enable single-line (DOTALL) mode so that `.` matches `\n`:

```rust
pub fn wildcard_regex(to_match: &str) -> Regex {
    Regex::new(&format!(
        "(?s)^{}$",
        regex::escape(to_match).replace("\\*", ".*")
    ))
    .expect("invalid wildcard regex")
}
```

With `(?s)`, `.` matches any character including `\n`, so `.*` crosses the newline and `$` matches at the true end of string. This is also the semantically correct behaviour: a wildcard `*` should match any content, including embedded or trailing newlines.

An alternative is to allow an optional trailing newline:

```rust
"^{}\n?$"
```

but this only handles the trailing-newline case and does not fix embedded newlines in multi-line values.

## Impact

Trailing newlines are common in log lines produced by Lambda runtimes, container stdout, and other line-delimited sources. Any Datadog Search Syntax filter applied to such field values will silently fail to match when wildcard queries are used.
