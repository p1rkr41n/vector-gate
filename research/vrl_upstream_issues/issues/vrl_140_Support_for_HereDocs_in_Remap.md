# [#140] Support for HereDocs in Remap

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/140)
- **Status**: `OPEN`
- **Author**: [@binarylogic](https://github.com/binarylogic)
- **Created At**: `2021-01-15T18:18:55Z`
- **Updated At**: `2026-06-01T14:16:10Z`
- **Comments**: 0
- **Labels**: `vrl:syntax`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/140)

---

## Description

HereDocs allow for the easy, and readable, creation of multi-line strings.

## Example

### Simple

```
"""
This is
a
long multi-line
string.
"""
```

Would produce:

```
"This is\na\nlong multi-line\nstring."
```

### Indentation preserved

```
"""
  This is
a
  long multi-line
string.
"""
```

Would produce:

```
"  This is\na\n  long multi-line\nstring."
```

### Leading white space ignored

```
.field = """
    This is
  a
    long multi-line
  string.
  """
```

Would produce:

```
"  This is\na\n  long multi-line\nstring."
```

Notice that the leading 2 spaces were trimmed since it did not align with the closing `"""` identifier.

## Requirements

- [ ] The leading `\n` should be stripped (as shown in the examples)
- [ ] The trailing \n` should be stripped (as shown in the examples)
- [ ] Program indentation should be ignored (spaces before the closing `"""`)
- [ ] Contained indentation should be preserved (beyond the close `"""`)
- [ ] New lines are preserved
