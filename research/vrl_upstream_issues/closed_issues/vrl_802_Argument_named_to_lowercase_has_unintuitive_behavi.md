# Issue #802: Argument named to_lowercase has unintuitive behavior

- **URL:** https://github.com/vectordotdev/vrl/issues/802
- **Author:** @andrewthad
- **Status:** CLOSED (completed)
- **Created:** 2024-04-18T15:00:10Z
- **Closed:** 2024-04-19T19:35:02Z
- **Labels:** None

## Description

I spent a while tracking down why something wasn't working, and the problem was that I had misunderstood the `convert_to_string` function:

```
pub(crate) fn convert_to_string(value: Value, to_lowercase: bool) -> Result<String, ValueError> {
    let string = value.try_bytes_utf8_lossy()?;
    Ok(match to_lowercase {
        true => string.to_string(),
        false => string.to_lowercase(),
    })
}
```

The argument `to_lowercase` can be used to convert the string to be converted to lowercase, but the caller must set it to `false` to do this! I suggest renaming this argument to `is_case_sensitive` or something like that to prevent confusion about its meaning.
