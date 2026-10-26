# [#102] Add explicit "enum type" to VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/102)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2021-07-28T09:06:15Z`
- **Updated At**: `2023-03-28T14:01:37Z`
- **Comments**: 2
- **Labels**: `type:enhancement`, `vrl:syntax`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/102)

---

## Description

We've been introducing functions that take an enum variant as an argument.

For example:

```coffee
parse_nginx_log(.message, format: "combined")
```

The `format` argument has to be either `"combined"` or `"error"`, and has to be a string literal. This has been awkwardly implemented and can be confusing to users. It also results in less-than-ideal error messages if people try to pass in non-literal string values (e.g. through an event field).

I've been pondering a solution, and although having full-blown enum support (both defining and referencing) can be powerful, I also believe it doesn't fit the simplicity we want to achieve with VRL.

Instead, I think we should add a new enum type that can only be referenced as a literal, similar to how we have a timestamp type.

Specifically, I propose we add `e'...'` as a type for an enum variant literal.

Given this function signature:

```coffee
foo(timestamp: Timestamp, variant: Enum)
```

You'd call this function like so:

```coffee
foo(timestamp: t'2021-01-01T00:00:00Z', variant: e'my_variant')
```

This would only compile if `variant` is passed an enum type (`e'...'`) _and_ if the provided enum variant is accepted by the function signature.

Function signatures would define the set of enum variants they accept, which the compiler can then automatically check (and provide useful error messages indicating which enum variants are expected and which one was provided). This is an improvement over the current situation because functions now have to build their own (non-ideal) error messages when dealing with enum-like strings, given that we don't actually have support for enums.

All of this would also bubble up into the Cue docs, which would result in better auto-generated function signatures and a list of enum variants supported for a specific parameter.
