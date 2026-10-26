# [#92] Dissallow `;` at the end of the last statement in an `if` predicate

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/92)
- **Status**: `OPEN`
- **Author**: [@StephenWakely](https://github.com/StephenWakely)
- **Created At**: `2021-09-20T16:18:42Z`
- **Updated At**: `2026-06-01T14:05:04Z`
- **Comments**: 0
- **Labels**: `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/92)

---

## Description

This parses and works fine in VRL:

```
x = 7
value = if (x = x + 1; x == 8;) {
  true
}
```

Arguably, we should error with the trailing `;` at the end of `x == 8`. This would be inline with Rust's treatment of `;`.

The problem is caused by the parsing rule:

```
    "(" <v:(<AssignmentExpr> ";")+> <e:(<AssignmentExpr>)?> ")" => {
```

With the trailing `;`, lalrpop juts puts all the statements into `v`, and leaves `e` as None. To fix this one would like to to remove the optional `?` from `e`. That would force the last line to be `e` and thus disallow the trailing `;`. However, this creates an ambiguity in the parsing rules and lalrpop refuses to build.


