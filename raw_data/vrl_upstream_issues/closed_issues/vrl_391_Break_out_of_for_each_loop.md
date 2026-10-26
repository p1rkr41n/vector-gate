# Issue #391: Break out of for_each loop

- **URL:** https://github.com/vectordotdev/vrl/issues/391
- **Author:** @mr-karan
- **Status:** CLOSED (completed)
- **Created:** 2023-08-17T13:25:27Z
- **Closed:** 2023-08-17T15:01:52Z
- **Labels:** None

## Description

I am trying to check if http_slug starts with any of the known paths (it's an array)  then assign that known value to http_slug_known. However I am not able to "stop" processing/enumerating subsequent items in the loop once the if condition has become true. I tried break keyword but it said it's unimplemented yet. Any thoughts on how can I achieve this?

```
# List of known paths
known_paths = [
    "/admin","/forgot", "/reset", "/logout", "/api"
]

http_slug_known = "unknown"
for_each(known_paths) -> |index, path| {
    if starts_with(to_string(http_slug), path) {
        http_slug_known = path
    }
}
```


Current Workaround:

```
found = false
for_each(known_paths) -> |index, path| {
    if !found && starts_with(to_string(http_slug), path) {
        http_slug_known = path
        found = true
    }
}
```

Would be nicer to have a `break` keyword implemented.
```[tasklist]
### Tasks
```

