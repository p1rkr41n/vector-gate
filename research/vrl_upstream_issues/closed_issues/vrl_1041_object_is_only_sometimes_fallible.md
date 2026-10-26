# Issue #1041: object() is only sometimes fallible

- **URL:** https://github.com/vectordotdev/vrl/issues/1041
- **Author:** @byronwolfman
- **Status:** CLOSED (completed)
- **Created:** 2024-09-18T15:02:33Z
- **Closed:** 2024-09-23T17:45:04Z
- **Labels:** None

## Description

Related to another issue, I'm running into a funny problem where the `object()` function is only sometimes fallible.

In an earlier transform, `.` has been turned into an object. Now in a new transform, we run into the following problems:

Fails `vector validate` because `.` is considered of type `any`:
```
redact(., filters: [...])
```

Ok, no problem. We'll ensure it's an object first! The following passes `vector validate` but now fails when tests are executed because `object!()` is considered infallible:

```
original = object!(.)
redact(original, filters: [...])
```

That's strange, because the docs mark `object()` as a fallible function. Ok, well, we could try to handle the error, but this doesn't work either because errors aren't returned for infallible functions:

```
original, err = object(.)
if err != null {
  abort
}
```

The reason seems to be that `object()` is considered _sometimes_ fallible:

```rust
impl FunctionExpression for ObjectFn {
    fn resolve(&self, ctx: &mut Context) -> Resolved {
        object(self.value.resolve(ctx)?)
    }

    fn type_def(&self, state: &state::TypeState) -> TypeDef {
        self.value
            .type_def(state)
            .fallible_unless(Kind::object(Collection::any()))
            .restrict_object()
    }
}
```

Given that I'm not sure how to actually use the function. It is only possible to get a passing `vector validate` and `vector test` if you pass a non-object, e.g. `object("definite-not-an-object")` so that it can be fallible for test+validate. If an object is passed in, it's still fallible for validate, but becomes infallible for test.
