# [#1537] unnest not preserving root field

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1537)
- **Status**: `OPEN`
- **Author**: [@objectbased](https://github.com/objectbased)
- **Created At**: `2025-10-14T00:28:06Z`
- **Updated At**: `2026-06-01T14:08:42Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`, `stdlib:unnest`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1537)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I'm currently working on a transform using remap/VRL to be able to take a batch of events and extract each of them into individual events for my downstream systems. I've noticed some weird behavior with the unnest command that I'm not entirely sure how to fix. Basically when a large of amounts of events come in from different sources all at the same time I'm finding that after my transform runs its VRL, sometimes the root level field "Authorization" which comes from the http_server source gets mixed up with other events "Authorizations" that pass through this transform.

For example, I have data source "A" coming in under "Authorization 123" and data source "B" coming in over "Authorization 456" and what I find is that periodically data source "A" will show data source "B" "Authorization" value. There are times in which the events do come in with the correct "Authorization" value to their respective events.

I've validated this at the sources and can confirm this is not happening there and when it does happen it only happens to events that come through this specific transform. To me it sounds like there is a race condition in which multiple different events come into the pipeline at the same time and unnesting causes these events to get mixed up in some way. I've attempt to preserve the "Authorization" value at the beginning of the transform and re-adding it back at the end, but that did not resolve the issue.

I have a very hard time reproducing this problem in my lower environment as I need to consistently have high volume of data coming through Vector at almost the exact same time for this to occur. However in production this occurs almost in real-time for feeds that produce well over 200GB an hour.

Any insight on the issue would be greatly appreciated.

### Configuration

```text
sources:
  http_source_server:
    type: http_server
    address: 0.0.0.0:443
    encoding: text
    headers:
      - User-Agent
      - Authorization
    auth:
      strategy: "custom"
    host_key: hostname
    method: POST
    path: /events
    path_key: path
    query_parameters:
      - application
    response_code: 200
    strict_path: false

event_endpoint_batched_events:
    type: remap
    inputs:
      - http_source_server
    drop_on_error: true
    reroute_dropped: true
    source: |-
      parts = split!(.message, r'\}\{')
      events = []
      for_each(array!(parts)) -> |index, part| {
      if index == 0 {
      part = part + "}"
      } else if index == length(parts) - 1 {
      part = "{" + part
      } else {
      part = "{" + part + "}"
      }
      parsed_event, parse_err = parse_json(part)
      parse_json, parse_json_err = parse_json(parsed_event.event)
      if parse_json_err != null {
        parsed_event_flatten, flatten_err = flatten(parsed_event.event)
        if flatten_err == null {
          parsed_event = parsed_event_flatten
        }
      } else {
        parsed_event = parse_json
      }

      events = push(events, parsed_event)
      }
      .message = events
      . = unnest!(.message)
```

### Version

Latest

### Debug Output

```text

```

### Example Data

Example event "A" and example event "B" (all events are on a single line)

{
  "Authorization": "test 123",
  "message": "{\"time\":1759280542.639, \"event\":{\"timeLogged\":\"2025-10-01 01:02:22.639\",\"source\":\"A\"}}{\"time\":1759280542.639, \"event\":{\"timeLogged\":\"2025-10-01 01:02:23.639\",\"source\":\"A\"}}{\"time\":1759280542.639, \"event\":{\"timeLogged\":\"2025-10-01 01:02:24.639\",\"source\":\"A\"}}"
}



{
  "Authorization": "test 456",
  "message": "{\"time\":1759280542.639, \"event\":{\"timeLogged\":\"2025-10-01 01:02:22.639\",\"source\":\"B\"}}{\"time\":1759280542.639, \"event\":{\"timeLogged\":\"2025-10-01 01:02:23.639\",\"source\":\"B\"}}{\"time\":1759280542.639, \"event\":{\"timeLogged\":\"2025-10-01 01:02:24.639\",\"source\":\"B\"}}"
}




### Additional Context

_No response_

### References

_No response_
