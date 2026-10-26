# [#111] confusing error messages in REPL mode regarding string error coalescing

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/111)
- **Status**: `OPEN`
- **Author**: [@jerome-kleinen-kbc-be](https://github.com/jerome-kleinen-kbc-be)
- **Created At**: `2021-05-26T19:07:31Z`
- **Updated At**: `2026-06-01T14:04:49Z`
- **Comments**: 2
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/111)

---

## Description

<!--
Hi there,

Thank you for opening an issue. Please note that we try to keep the Vector issue tracker reserved for bug reports and feature requests. For general usage questions, please see: https://chat.vector.dev.
-->

### Vector Version

<!---
Run `vector --version` to show the version, and paste the result between the ``` marks below.

If you are not running the latest version of Vector, please try upgrading because your issue may have already been fixed.
-->

```
vector 0.13.1 (v0.13.1 x86_64-apple-darwin 2021-04-29)
```

### Vector Configuration File

<!--
Paste the relevant parts of your `vector.toml` configuration between the ``` marks below.

!! If your config files contain sensitive information please remove it !!
-->

Not applicable, but run the following commands in REPL mode:
```
.message = "abc"
match(string(.message) ?? "", r'a')
```

### Debug Output

<!--
Full debug output can be obtained by running Vector with the following:

```
RUST_BACKTRACE=full vector -vvv <rest of commands>
```

Please create a GitHub Gist containing the debug output. Please do _not_ paste the debug output in the issue, since debug output is long.

!! Debug output may contain sensitive information. Please review it before posting publicly. !!
-->


### Expected Behavior

To be honest, I think the REPL mode should allow this notation to be more in line with testing real life events, or it should give the following error

```
error[E651]: unnecessary error coalescing operation
  ┌─ :1:7
  │
1 │ match(string(.message) ?? "", r'a')
  │       ^^^^^^^^^^^^^^^^ -- -- this expression never resolves
  │       │                │
  │       │                remove this error coalescing operation
  │       this expression can't fail
  │
  = see language documentation at https://vrl.dev
```

Perhaps this error should be warning instead?

### Actual Behavior

vector throws the following two errors:

```
error[E651]: unnecessary error coalescing operation
  ┌─ :1:7
  │
1 │ match(string(.message) ?? "", r'a')
  │       ^^^^^^^^^^^^^^^^ -- -- this expression never resolves
  │       │                │
  │       │                remove this error coalescing operation
  │       this expression can't fail
  │
  = see language documentation at https://vrl.dev

error[E110]: invalid argument type
  ┌─ :1:7
  │
1 │ match(string(.message) ?? "", r'a')
  │       ^^^^^^^^^^^^^^^^^^^^^^
  │       │
  │       this expression resolves to the exact type "boolean"
  │       but the parameter "value" expects the exact type "string"
  │
  = try: ensuring an appropriate type at runtime
  =
  =     null == null = string!(null == null)
  =     match(null == null, a)
  =
  = try: coercing to an appropriate type and specifying a default value as a fallback in case coercion fails
  =
  =     null == null = to_string(null == null) ?? "default"
  =     match(null == null, a)
  =
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = learn more about error code 110 at https://errors.vrl.dev/110
  = see language documentation at https://vrl.dev
```

The second warning is rather confusing: `string(.message) ?? ""` would never result in a boolean

### Example Data

<!--
Please provide any example data that will help debug the issue, for example:

```
201.69.207.46 - kemmer6752 [07/06/2019:14:53:55 -0400] "PATCH /innovative/interfaces" 301 669
```
-->

### Additional Context

<!--
Is there anything atypical about your situation that we should know? For example: is Vector running in Kubernetes? Are you passing any unusual command line options or environment variables to opt-in to non-default behavior?
-->

### References

<!--
Are there any other GitHub issues (open or closed) or Pull Requests that should be linked here? For example:

- vectordotdev/vector#6017

-->

