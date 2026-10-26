# Issue #453: Error message loop with variables in closures

- **URL:** https://github.com/vectordotdev/vrl/issues/453
- **Author:** @lukesteensen
- **Status:** CLOSED (completed)
- **Created:** 2023-09-15T09:10:08Z
- **Closed:** 2026-05-01T20:53:45Z
- **Labels:** vrl:compiler

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

It appears that the compiler is unable to reason about types vs fallibility for variables in closures. It returns an error message saying something is fallible, then when the corresponding change is made it then shows an error that it is infallible. It's not clear how to work around these errors and satisfy the compiler.

### Configuration

```text
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoib3V0cHV0ID0gW11cbmZvcl9lYWNoKC4pIC0%2BIHxrZXksIHZhbHVlfCB7XG4gICAgZSA9IHt9XG4gICAgc2V0KGUsIFtrZXldLCB2YWx1ZSlcbiAgICBvdXRwdXQgPSBwdXNoKG91dHB1dCwgZSlcbn1cbi4gPSBvdXRwdXQiLCJldmVudCI6eyJmb28iOiJvbmUiLCJiYXIiOiJ0d28iLCJiYXoiOiJ0aHJlZSJ9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

output = []
for_each(.) -> |key, value| {
    e = {}
    set(e, [key], value)
    output = push(output, e)
}
. = output
```


### Version

Vector 0.32.0
VRL 0.6.0

### Debug Output

```text
error[E103]: unhandled fallible assignment
  ┌─ :5:14
  │
5 │     output = push(output, e)
  │     -------- ^^^^^^^^^^^^^^^
  │     │        │
  │     │        this expression is fallible
  │     │        update the expression to be infallible
  │     or change this to an infallible assignment:
  │     output, err = push(output, e)
  │
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = learn more about error code 103 at https://errors.vrl.dev/103
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```


### Example Data

```
{
    "foo": "one",
    "bar": "two",
    "baz": "three"
}
```

### Additional Context

_No response_

### References

_No response_
