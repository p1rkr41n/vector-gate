# Issue #448: Allow using strings as json paths

- **URL:** https://github.com/vectordotdev/vrl/issues/448
- **Author:** @ayZagen
- **Status:** CLOSED (completed)
- **Created:** 2023-09-12T11:22:58Z
- **Closed:** 2023-09-12T12:40:20Z
- **Labels:** None

## Description

Currently vrl functions accepts query paths defined in jq like statements. However using strings as json paths is the most common way to interact with jsons

By accepting strings we could write functions like this:

```lua
fields = [".source_type", ".kubernetes.pod_ip"]
for_each(fields) -> |_index, value| {
  del(value)
}
``` 

Strictly related to #25
