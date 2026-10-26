# Issue #381: Flatten does not work as expected when using a top-level field from a vector message

- **URL:** https://github.com/vectordotdev/vrl/issues/381
- **Author:** @teeohhem
- **Status:** CLOSED (completed)
- **Created:** 2023-08-14T17:02:08Z
- **Closed:** 2023-08-16T16:25:53Z
- **Labels:** None

## Description

When using the flatten operation, referencing a field (that contains an object) from an event results in a no-op. This is because when you reference a field from a vector event, you are just given the value, which in this case, is just an object without a key. Therefore, obviously, there is nothing to flatten.

I personally would expect the flatten operation to "just work" and flatten with the key into the main event.

Here's an example: 

Event
```
{
    "timestamp": 1245542,
    "errors": {
        "code": 1234,
        "message": "invalid type",
        "class": "EventHelper"
    },
    "otherKey:" {
        "id": 1
    }
}
```

VRL
```
    flattened,err = flatten(.errors)
```

Expected: 
```
{
    "timestamp": 1245542,
    "errors.code": 1234,
    "errors.message": "Invalid type",
    "errors.class": "EventHelper",
    "otherKey:" {
        "id": 1
    }
}
```

Actual: 
No change to the event.


