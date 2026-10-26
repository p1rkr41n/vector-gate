# Issue #394: Deep iterate over key/value pairs in an object

- **URL:** https://github.com/vectordotdev/vrl/issues/394
- **Author:** @ayZagen
- **Status:** CLOSED (completed)
- **Created:** 2023-08-17T18:27:00Z
- **Closed:** 2023-08-17T19:27:49Z
- **Labels:** type:enhancement

## Description

I have seen some issues regarding this and they refer to `map_values`, `map_keys` and `redact` functions but all of them falls short on for this.

Let's assume we have a log entry as below and we would like to transform it to ensure data safety and regulations such as GDPR.
Here is input:
```json
{
  "user": {
    "email": "john@doe.com",
    "phone_number": "+1 (123) 232 11 11",
  },
  "event_details": {
     "provider": {
        "settings": {
           "api_key": "MY_SECRET_KEY",
           "api_url": "https://myapiurl.com"
        },
     }
  }
}
```

And here is an expected result:
```json
{
  "user": {
    "email": "j***@d**.com",
    "phone_number": "+1 (1**) *** ** 11",
  },
  "event_details": {
     "provider": {
        "settings": {
           "api_key": "HIDDEN",
           "api_url": "https://myapiurl.com"
        },
     }
  }
}
```

Currently only way to reach this result is by checking with `exists` and applying modification. Imagine you have lots of keys to be checked, our vrl script will be full of if checks.

But if we had a way to reach to path in `map_values` it would cover almost all cases. With this way we could provide lots of keys easily.

For ex:
```
to_be_redacted = [ "event_details.provider.settings.api_key" ]
to_be_masked = {
  "user.email": "regex_here"
}

map_values(.) -> |value, key, path| { 
  if( includes( to_be_redacted, path ) ) {
    "HIDDEN"
  } else if ( includes( keys(to_be_masked), path ) ) {
    r = to_regex!( get!(value: to_be_masked, path: split(path, "." ) ) )
    replace(value, r)
  } else {
    value
  }
}
```

Please consider this. Thanks
