# [#1040] Determining if redact has redacted

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1040)
- **Status**: `OPEN`
- **Author**: [@byronwolfman](https://github.com/byronwolfman)
- **Created At**: `2024-09-18T13:58:31Z`
- **Updated At**: `2024-09-23T17:09:54Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1040)

---

## Description

Our team has been playing around with `redact` and something we're trying to wrap our heads around is how to determine if `redact` has modified the input. This is straightforward when the input is a string, but we're not sure what to do with objects. We've tried abusing `assert_eq` but the docs recommend against using assertions outside of unit tests.

An "easy" way around this problem would be if `redact` could return two values:

1. The `<string | object | array>` output as usual
2. A `<boolean>` indicating whether or not the output has changed

The workaround I can see for now is something along the lines of

```
redacted = redact(., [r'\d+'])

if encode_json(.) != encode_json(redacted) {
    . = redacted
    .tags = ["redacted:number"]
}
```

My hesitation is that I'm not sure how expensive it is to marshal JSON twice on every log event, especially as we're operating at a decently large scale. On the other hand, Vector has made me into a Rust true believer, and maybe I'm over-thinking the performance implications.
