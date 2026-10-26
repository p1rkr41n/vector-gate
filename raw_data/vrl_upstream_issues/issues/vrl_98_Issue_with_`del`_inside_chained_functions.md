# [#98] Issue with `del` inside chained functions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/98)
- **Status**: `OPEN`
- **Author**: [@spencergilbert](https://github.com/spencergilbert)
- **Created At**: `2021-08-16T15:27:56Z`
- **Updated At**: `2026-06-16T13:11:23Z`
- **Comments**: 5
- **Labels**: `vrl:compiler`, `stdlib:del`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/98)

---

## Description

Ex:

```shell
$ .message = "{\"foobar\": \"baz\"}"
"{\"foobar\": \"baz\"}"

$ . |= object!(parse_json!(del(.message)))
{ "foobar": "baz", "message": "{\"foobar\": \"baz\"}" }
```

## Workaround

Move `del` function to a separate line either like:

```vrl
msg = del(.message)
. |= object!(parse_json!(msg))
```

or

```vrl
. |= object!(parse_json!(.message))
del(.message)
```
