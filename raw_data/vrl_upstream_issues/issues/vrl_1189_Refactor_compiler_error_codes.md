# [#1189] Refactor compiler error codes

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1189)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2024-12-12T20:52:33Z`
- **Updated At**: `2024-12-12T20:52:40Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`, `type:tech debt`, `good first issue`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1189)

---

## Description

### The Problem

Currently we assign arbitrary error codes in different modules e.g.

```
    fn code(&self) -> usize {
        // ...
        match self {
            Undefined { .. } => 105,
            WrongNumberOfArgs { .. } => 106,
            UnknownKeyword { .. } => 108,
            Compilation { .. } => 610,
            // ...
        }
    }
```

These codes are scattered across different files and there's nothing preventing us from reusing them. 

### Solution
We should aggregate these under a single enum in `src/compiler/errors`. 

Without giving this too much thought (might revisit later), we can have static arrays of codes:
```
const FUNCTION_CALL_ERROR_CODES: &[(FunctionCallError, usize)] = &[
    (Undefined, 105),
    (WrongNumberOfArgs, 106),
    (UnknownKeyword, 108),
    (Compilation, 610),
    // ...
];
```

and then use them like so:
```
impl DiagnosticMessage for FunctionCallError {
    fn code(&self) -> usize {
        use FunctionCallError::*;

        FUNCTION_CALL_ERROR_CODES
            .iter()
            .find(|&&(ref variant, _)| variant == self)
            .map(|&(_, code)| code)
            .expect("Error code not found for FunctionCallError variant")
    }
}
```

### Docs

If we find duplicates and have to re-assign codes, we will also need to update:
https://vector.dev/docs/reference/vrl/errors/#compile-time-errors

Changing codes assigned to errors IMO isn't a breaking change. 

> To VRL users, if you use these codes, please comment in this ticket!

### References
Ideally these should be generated from code, see https://github.com/vectordotdev/vrl/issues/280.
