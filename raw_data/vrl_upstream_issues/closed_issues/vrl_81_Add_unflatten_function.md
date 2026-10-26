# Issue #81: Add `unflatten` function

- **URL:** https://github.com/vectordotdev/vrl/issues/81
- **Author:** @jszwedko
- **Status:** CLOSED (completed)
- **Created:** 2022-01-27T20:04:51Z
- **Closed:** 2024-08-27T21:46:29Z
- **Labels:** vrl:stdlib

## Description

<!--
Hi there,

Thank you for opening an issue. Please note that we try to keep the Vector issue tracker reserved for bug reports and feature requests. For general usage questions, please see: https://chat.vector.dev.
-->

<!--- Please keep this note for the community --->

### Community Note

* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment

<!--- Thank you for keeping this note for the community --->

### Current Vector Version

<!---
Run `vector --version` to show the version, and paste the result between the ``` marks below. This will record which version was current at the time of your feature request, to help manage the request backlog.

If you're not using the latest version, please check to see if something related to your request has already been implemented in a later version.
-->

```
vector 0.19.1 (x86_64-apple-darwin 3cf70cf 2022-01-25)
```

### Use-cases

We have a `flatten` function that flattens objects by joining together nested keys with `.`. It'd be useful to have a way to reverse this. This could also be useful for sources of data that use `.`s in keys.


See https://github.com/vectordotdev/vector/discussions/11062

### Attempted Solutions

This `lua` transform works:

```toml
[transforms.nest]
type = "lua"
inputs = ["stdin"]
version = "2"
source = '''
function build_array(...)
  local arr = {}
  for v in ... do
    arr[#arr + 1] = v
  end
  return arr
end

function process(event, emit)
  for key, value in pairs(event.log) do
    event.log[key] = value

    parts = build_array(string.gmatch(key, "[^\\.]+"))

    -- key has a dot in it, break it apart to create nested table
    if #parts > 1 then
      event.log[key] = nil

      to_update = event.log
      for i = 1, #parts - 1 do
        if to_update[parts[i]] == nil then
          to_update[parts[i]] = {}
        end
        to_update = to_update[parts[i]]
      end
      to_update[parts[#parts]] = value
    end
  end
  emit(event)
end
'''
hooks.process = "process"
```

### Proposal

We add a `unflatten` function to VRL that does the opposite of `flatten`.

### References

<!--
Are there any other GitHub issues, whether open or closed, that are related to the problem you've described above or to the suggested solution? If so, please create a list below that mentions each of them. For example:

- vectordotdev/vector#7023

-->

