# [#850] for_each doesn't affect type

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/850)
- **Status**: `OPEN`
- **Author**: [@Rajin9601](https://github.com/Rajin9601)
- **Created At**: `2024-05-21T07:02:50Z`
- **Updated At**: `2026-06-16T13:09:57Z`
- **Comments**: 1
- **Labels**: `vrl:compiler`, `stdlib:for_each`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/850)

---

## Description

```
body = del(.)
for_each(["test1"]) -> |key, path| {
  ., err = set(., ["new", path], "test1")
}
.new.test2 = "test2"
```
this VRL program fails in compiling because of type of `.new`. ([VRL Playground Link](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiYm9keSA9IGRlbCguKVxuZm9yX2VhY2goW1widGVzdDFcIl0pIC0%2BIHxrZXksIHBhdGh8IHtcbiAgLiwgZXJyID0gc2V0KC4sIFtcIm5ld1wiLCBwYXRoXSwgXCJ0ZXN0MVwiKVxufVxuLm5ldy50ZXN0MiA9IFwidGVzdDJcIiIsImV2ZW50Ijp7Im1lc3NhZ2UiOiJIZWxsbyBWUkwiLCJmb28iOiJkZWxldGUgbWUiLCJodHRwX3N0YXR1cyI6IjIwMCJ9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D))

Error Log
```
error[E642]: parent path segment rejects this mutation
  ┌─ :5:6
  │
5 │ .new.test2 = "test2"
  │ ---- ^^^^^ querying a field of a non-object type is unsupported
  │ │
  │ this path resolves to a value of type undefined
  │
  = try: change parent value to object, before assignment
  =
  =     .new = {}
  =     .new.test2 = "test2"
  =
  = see documentation about error handling at https://errors.vrl.dev/#handling
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

However, if it's inside an if statement instead of for_each, this vrl program can be compiled.
```
body = del(.)
if is_boolean(body.message) {
    ., err = set(., ["new", "test1"], "test1")
}
.new.test2 = "test2"
```
[VRL Playground link](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiYm9keSA9IGRlbCguKVxuaWYgaXNfYm9vbGVhbihib2R5Lm1lc3NhZ2UpIHtcbiAgICAuLCBlcnIgPSBzZXQoLiwgW1wibmV3XCIsIFwidGVzdDFcIl0sIFwidGVzdDFcIilcbn1cbi5uZXcudGVzdDIgPSBcInRlc3QyXCIiLCJldmVudCI6eyJtZXNzYWdlIjoiSGVsbG8gVlJMIiwiZm9vIjoiZGVsZXRlIG1lIiwiaHR0cF9zdGF0dXMiOiIyMDAifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D)

My theory is that `.`'s type is not changed by the for_each statement, which looks like a bug.
