# [#1084] Whitespace required around `!=` operator

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1084)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2024-10-22T15:38:37Z`
- **Updated At**: `2026-06-01T14:08:00Z`
- **Comments**: 0
- **Labels**: `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1084)

---

## Description

The following:

```
 .ddtags.kube_namespace=="kong" &&  .message!="[notice] 2383#0:4 [lua] init.lua:272:"
```

Gives the error:

```

error[E203]: syntax error
  ┌─ :1:38
  │
1 │  .ddtags.kube_namespace=="kong" &&  .message!="[notice] 2383#0:4 [lua] init.lua:272:"
  │                                      ^^^^^^^
  │                                      │
  │                                      unexpected syntax token: "FunctionCall"
  │                                      expected one of: ".", "[", "abort", "identifier", "path field", "return", "string literal", RQuery
  │
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

Adding whitespace around the `!=` seems to fix it:

```
 .ddtags.kube_namespace=="kong" &&  .message != "[notice] 2383#0:4 [lua] init.lua:272:"
```
