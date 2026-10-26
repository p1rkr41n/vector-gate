# [#149] Change VRL to support compile-time-only functions, needed for semantic meaning functions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/149)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-02-10T15:26:50Z`
- **Updated At**: `2023-03-28T14:40:03Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/149)

---

## Description

I realized that the function I built (`set_field_purpose`) is a “compile-time only” function. That is, it does something with the type state of VRL, but doesn’t do anything at runtime. It’s not a “runtime function that can also run at compile time”, it’s a “compile time function that cannot run at runtime”.  Or, to be more exact, it’s a no-op at runtime.

The implication here is that this function must be called in a non-dynamic context; otherwise you end up with unexpected results.

Take for example this:

```coffee
if .foo == true {
	set_field_purpose(.foo, "bar")
}
```

The `set_field_purpose` function does its job when VRL compiles, but VRL compilation obviously can’t consider run-time information, so it compiles `set_field_purpose` which then modifies the schema in Vector.

The operator writing this might expect that function to only do something if `.foo` returns `true`, but that’s not possible because we need that function to execute at compile-time, for the schema to work when Vector boots.

The solution here is to add a new check to the compiler, which keeps track of each root expression, and makes sure that there’s no compile-time-only expression nested in a runtime expression. So, this compiles:

```coffee
set_field_purpose(.foo, “bar”)
if .foo == true {
	log(“yep”)
}
```

But this doesn’t:

```coffee
if .foo == true {
	set_field_purpose(.foo, “bar”)
	log(“yep”)
}
```

For now, we can keep the initial implementation simple, and just never allow a compile-time expression to be mixed with any other expressions, but in the future we can expand this to basically support “const” similar to Rust, in which some expressions can _also_ be used at compile time, with the addition in our case that we also have the constraint that some expressions can _only_ be used at compile time (such as `set_field_purpose`), not saying we _should_ do this, but it’s a possibility that remains open to us.

Anyway, long story short, for us to allow VRL to manipulate semantic meaning of schema fields (which we’d need to allow people to manually map from one schema to another), we need to add an initial bare-bones feature that supports the above use-case.

Unless, of course, anyone has a better idea that would be simpler to do as an initial pass, without causing too much hackery and/or breaking changes.

Of course, the most simple solution is to “not care” about the above confusion, and simply document for now that this function does not interact with other dynamic expressions.
