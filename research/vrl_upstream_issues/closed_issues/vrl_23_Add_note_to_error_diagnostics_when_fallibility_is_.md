# Issue #23: Add note to error diagnostics when fallibility is due to function arguments

- **URL:** https://github.com/vectordotdev/vrl/issues/23
- **Author:** @jszwedko
- **Status:** CLOSED (completed)
- **Created:** 2022-09-16T13:28:32Z
- **Closed:** 2023-11-14T20:42:33Z
- **Labels:** vrl:compiler

## Description

Users are frequently confused when a function marked is infallible in the docs is fallible because of the types of its arguments. The error message looks like:

```
  error[E103]: unhandled fallible assignment
    ┌─ :7:30
    │
  7 │         .splunk_sourcetype = downcase(type)
    │         -------------------- ^^^^^^^^^^^^^^
    │         │                    │
    │         │                    this expression is fallible
    │         │                    update the expression to be infallible
    │         or change this to an infallible assignment:
    │         .splunk_sourcetype, err = downcase(type)
    │
    = see documentation about error handling at https://errors.vrl.dev/#handling
    = learn more about error code 103 at https://errors.vrl.dev/103
    = see language documentation at https://vrl.dev
    = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

I think helpful if the diagnostics mentioned the fallibility is due to the type of the function arguments and, perhaps, included a link to https://vector.dev/docs/reference/vrl/expressions/#function-call-characteristics.
