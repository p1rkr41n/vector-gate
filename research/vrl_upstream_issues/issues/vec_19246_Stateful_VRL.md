# [#19246] Stateful VRL

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/19246)
- **Status**: `OPEN`
- **Author**: [@splitice](https://github.com/splitice)
- **Created At**: `2023-11-27T23:37:33Z`
- **Updated At**: `2026-06-05T22:29:20Z`
- **Comments**: 2
- **Labels**: `meta:idea`, `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/19246)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

As per the comment on the lua module page I thought I would share what we are doing with the lua module that is not currently possible with other transforms (including VRL).

See attempted solution for the LUA code we are using

Why are we doing this? Because Loki querying scales poorly when chunks get too dense. Most of the time its benificial to fill massive chunks, but if the event rate peaks high it makes sense to fill out additional chunks in parallel to spread the load between ingesters and on querying provide additional parallelisation. Segment becomes a label in this application.

### Attempted Solutions

```
  function init()
  map_rate = {}
  map_result = {}
  math.randomseed(os.time())
  end

  function process(event, emit)
  local key = [key representing appropriate parts of the event]

  if map_rate[key] == nil then
    map_rate[key] = 1
  else
    map_rate[key] = map_rate[key] + 1
  end

  local max_count = map_result[key] 
  if max_count == nil then
    event.log.segment = 0
  else
    event.log.segment = math.random(0, max_count)
  end
  emit(event)
  end
  
  function timer_handler(emit)
  for k,v in pairs(map_rate) do
    local result = math.floor(map_rate[k] / 6000)
    if result > 0 then
      map_result[k] = result
    end
    map_rate[k] = 0
  end
  end
```

### Proposal

This isnt something VRL can do as VRL is entirely stateless. Perhaps then there is room for a stateful VRL transform and a stateless? Or a flag on VRL to enable a global table?

### References

_No response_

### Version

0.32
