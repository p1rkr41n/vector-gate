# [#501] Make is_json more permissive

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/501)
- **Status**: `OPEN`
- **Author**: [@saliagadotcom](https://github.com/saliagadotcom)
- **Created At**: `2023-10-10T19:07:10Z`
- **Updated At**: `2026-06-16T13:10:18Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:is_json`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/501)

---

## Description

Currently the documentation states `is_json` is a infallible function call. However passing in a argument without casting as a  string will fail
```~/Development/ccd-security-lake shend/okta *+ env DATADOG_API_KEY_ENV_VAR=TEST vector test /Users/shend/Development/ccd-security-lake/generated/staging/okta.yaml
Running tests
2023-10-10T18:25:59.580454Z ERROR vector::unit_test: Failed to execute tests:
Failed to build test 'test_transforms':
  failed to create test condition '0': 
  error[E630]: fallible argument
    ┌─ :1:9
    │
  1 │ assert!(is_json(.actor))
    │         ^^^^^^^^^^^^^^^
    │         │
    │         this expression can fail
    │         handle the error before passing it in as an argument
    │
    = see documentation about error handling at https://errors.vrl.dev/#handling
    = see language documentation at https://vrl.dev
    = try your code in the VRL REPL, learn more at https://vrl.dev/examples
  .
~/Development/ccd-security-lake shend/okta *+ vector --version
vector 0.33.0 (x86_64-apple-darwin 89605fb 2023-09-27 14:18:24.180809939)
```

When casting the argument as a string using `string!` it passes
```
assert!(is_json(string!(.actor)))
```

Would it make sense to have is_json() check if the argument as a string and return false if its not? 
