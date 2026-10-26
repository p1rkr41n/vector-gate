# [#116] fields extracted using parse_regex imply incorrect type definitions when parse_regex fails

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/116)
- **Status**: `OPEN`
- **Author**: [@jerome-kleinen-kbc-be](https://github.com/jerome-kleinen-kbc-be)
- **Created At**: `2021-05-11T12:55:37Z`
- **Updated At**: `2026-06-16T13:11:30Z`
- **Comments**: 5
- **Labels**: `vrl:typedef`, `stdlib:parse_regex`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/116)

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
vector 0.13.1 (v0.13.1 x86_64-unknown-linux-gnu 2021-04-29)
```

### Vector Configuration File

<!--
Paste the relevant parts of your `vector.toml` configuration between the ``` marks below.

!! If your config files contain sensitive information please remove it !!
-->

```toml
[sources.generator]
  type = "generator"
  format = "syslog"
  
[transforms.remap]
  type = "remap"
  inputs = ["generator"]
  source = '''
  . |= parse_regex(.message, r'^<\d+>(?P<a>\S+') ?? {}
  .a = downcase(string(.a) ?? "")
  '''
  
[sinks.console]
  type = "console"
  inputs = ["remap"]
  encoding = "json"
```

### Debug Output

```
error[E651]: unnecessary error coalescing operation
  ┌─ :2:17
  │
2 │   .a = downcase(string(.a) ?? "")
  │                 ^^^^^^^^^^ -- -- this expression never resolves
  │                 │          │
  │                 │          remove this error coalescing operation
  │                 this expression can't fail
  │
  = see language documentation at https://vrl.dev

error[E110]: invalid argument type
  ┌─ :2:17
  │
2 │   .a = downcase(string(.a) ?? "")
  │                 ^^^^^^^^^^^^^^^^
  │                 │
  │                 this expression resolves to the exact type "boolean"
  │                 but the parameter "value" expects the exact type "string"


```


### Expected Behavior

Config should work as expected.

### Actual Behavior

Config returns an error when using vector validate or running the config.

### Example Data

Generated data.

### Additional Context

Discussed this with @JeanMertz and he figured out that vector is making a wrong compile time assumption of the fields extracted using regex capture groups when parse_regex errors are suppressed using the " ?? {} " notation used above. A potential workaround is:

```toml
[sources.generator]
  type = "generator"
  format = "syslog"
  
[transforms.remap]
  type = "remap"
  inputs = ["generator"]
  source = '''
  . |= parse_regex(.message, r'^<\d+>(?P<a>\S+') ?? {"a": null}
  .a = downcase(string(.a) ?? "")
  '''
  
[sinks.console]
  type = "console"
  inputs = ["remap"]
  encoding = "json"
```

### References

Discussed on Discord in the support channel on 11/05/2021 around 12:00 CET.

