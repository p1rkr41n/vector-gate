# Issue #7044: VRL Contains function wrong case_sensitive default value

- **URL:** https://github.com/vectordotdev/vector/issues/7044
- **Author:** @SyluxDX
- **Status:** CLOSED (completed)
- **Created:** 2021-04-08T11:44:17Z
- **Closed:** 2021-04-16T18:00:07Z
- **Labels:** domain:vrl

## Description

On the [Contains Documentation](https://vector.dev/docs/reference/vrl/functions/#contains) states that the default value for the case_sensitive argument is `True` but when testing the actual default value is `False`

### Vector Version
```
0.12.2
```

### Expected Behavior

```
$ contains("The Needle In The Haystack", "Needle")
true

$ contains("The Needle In The Haystack", "needle")
false
```

### Actual Behavior

```
$ contains("The Needle In The Haystack", "Needle")
true

$ contains("The Needle In The Haystack", "needle")
true
```

### Example using event

```
$ .message
"4.46.4.m.prod-b [15467.608359] ### Error at magnum/portinginterface/hdm/src/common/bhdm_hdcp.c:375"

$ contains!(.message, "error")
true

$ contains!(.message, "Error")
true

$ contains!(.message, "error", false)
true

$ contains!(.message, "error", true)
false
```

