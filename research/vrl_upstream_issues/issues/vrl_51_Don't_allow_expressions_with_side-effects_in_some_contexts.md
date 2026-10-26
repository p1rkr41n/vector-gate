# [#51] Don't allow expressions with side-effects in some contexts

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/51)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-06-17T00:59:58Z`
- **Updated At**: `2026-06-01T14:17:02Z`
- **Comments**: 1
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/51)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Expressions containing side-effects can be ambiguous/confusing when used in certain contexts.  
Consider the following example.

```coffeescript
. = { "msg": "{\"a\":1}" }
. |= object!(parse_json!(del(.msg)))
```

You might assume the event would look like this after running
```coffeescript
{ "a": 1 }
```

but it's actually
```coffeescript
{ "a": 1, "msg": "{\"a\":1}" }
```

To understand this better, you can look at the "de-sugared" version of the 2nd line,
```coffeescript
. = . | object!(parse_json!(del(.msg)))
```

The merge operator (`|`) has 2 arguments, and it resolves them from left to right. The first is the event itself, which is _copied_.
Then the 2nd is resolved, which calls `del(.msg)` first, then parses the json. The `del` deletes `.msg` _after_ `.` has already been copied. The two arguments are then merged, and the result is assigned back to `.`.

Now if you switched the ordering to this
```coffeescript
. = object!(parse_json!(del(.msg))) | .
```

It would result in
```coffeescript
{ "a": 1 }
```


### Proposal

Expressions containing "side-effects" (assignments, and behaviors such as logging) should be forbidden in certain situations. This should not reduce the power of VRL, but rather require you to re-write in ways that are more clear (which the compiler should usually help with). The list of places this will be forbidden is TBD, but will likely include things like function arguments and operator inputs.

The above example should be re-written as
```coffeescript
msg = del(.msg)
. |= object!(parse_json!(msg))
```

which more unambiguously deletes from `.msg` _first_, and then parses and merges the result. The event would end up looking like this

```coffeescript
{ "a": 1 }
```

Non-exhuastive list of areas this should apply to:
- creating objects (the order of resolving fields is not clearly defined, but is currently "alphabetical" which can be confusing)
- creating arrays
- function arguments
- all operators? (addition, multiplication, merge, etc.)

