# [#1949] `slice!()` operates on bytes, not characters, silently corrupts multi-byte strings

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1949)
- **Status**: `OPEN`
- **Author**: [@28515graj](https://github.com/28515graj)
- **Created At**: `2026-09-15T19:43:52Z`
- **Updated At**: `2026-09-17T18:10:58Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1949)

---

## Description


**Vector version:** 0.58.0 (VRL 0.35.0)

**Severity:** Major (silent data corruption in line decoding)

**Description:**

When using `slice!()` on a UTF-8 string with multi-byte characters (BOM, emoji, CJK), it counts BYTES not characters.

**Source code (confirmed in VRL 0.35.0):**
`vrl/src/stdlib/slice.rs:68`:
```rust
Value::Bytes(v) => range(v.len() as i64)
    .map(|range| v.slice(range))
    .map(Value::from),
```

`v.len()` returns byte length, then `v.slice(range)` indexes by bytes. For multibyte UTF-8 characters this splits codepoints mid-sequence.

**Reproduction (Vector vrl REPL):**

```vrl
.s = "abc"  # 3 bytes / 3 chars
.slice1_repr = slice!(.s, 1)  # expect "bc", got: "bc"
```

Try with multi-byte characters:
```vrl
.s = "AAAAA"  # 5 chars (each A is 4 bytes UTF-8 = 20 bytes total)
.slice1 = slice!(.s, 1)  # not "AAAA" -- instead first chars are corrupted UTF-8
.slice1_len = length(.slice1)
# Original: 5 chars (length 5)
# After slice 1: length = 19 chars (next chars are partial UTF-8 sequences)
```

**Expected behavior:**

The documentation should clarify that `slice!()` is byte-based.
Ideally add a `slice_chars!()` function that operates on UTF-8 character indices, or have `slice!()` automatically detect UTF-8 boundaries.

**Workaround:**

Manually count bytes for known multi-byte sequences:
- UTF-8 BOM = 3 bytes (`EF BB BF`)
- CJK chars = 3 bytes each
- Emoji = 4 bytes each (some up to 8)

```vrl
# Remove 3-byte UTF-8 BOM
raw_line = slice!(string!(.message), 3)
```

**Impact:**

CSV/TSV pipelines that handle UTF-8 BOM (Excel-exported files), CJK content, or emojis produce corrupted output when slicing.

**Confirmed in source:** `vrl/src/stdlib/slice.rs:68` (Vector 0.58.0, VRL 0.35.0)
