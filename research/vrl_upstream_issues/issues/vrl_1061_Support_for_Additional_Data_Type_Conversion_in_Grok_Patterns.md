# [#1061] Support for Additional Data Type Conversion in Grok Patterns

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1061)
- **Status**: `OPEN`
- **Author**: [@Anton0C](https://github.com/Anton0C)
- **Created At**: `2024-10-02T09:30:13Z`
- **Updated At**: `2024-10-02T14:16:48Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1061)

---

## Description

### Description:
It would be beneficial to extend Grok’s current functionality by allowing users to specify the type of attribute value to extract. At present, all semantic values are stored as strings by default. However, users might want to convert the extracted values into different data types for further processing.

### Proposed Enhancement:
Add support for additional data type conversions within Grok patterns. Users can specify the target data type by suffixing the semantic in the pattern, such as `%{NUMBER:num:int}` to convert the num semantic from a string to an integer.

For instance, this pattern:
```
%{NUMBER:Basic:float} %{NUMBER:Basic_long:long}
```
would convert the Basic semantic to a float and Basic_long to a long integer 🌟 
