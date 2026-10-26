# [#17082] Assigning the result of compact to the root of a metric event quietly fails

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/17082)
- **Status**: `OPEN`
- **Author**: [@martinwaite](https://github.com/martinwaite)
- **Created At**: `2023-04-07T15:24:27Z`
- **Updated At**: `2026-02-21T20:39:53Z`
- **Comments**: 1
- **Labels**: `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/17082)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I'm trying to use Vector (0.28.1) to clean empty values from metrics events.

I tried the following remap source `. = compact(.)`  but this left the empty tags in place.  

The workaround is `.tags, err = compact(.tags)` which is ok, but I was surprised that `. = compact(.)`  doesn't work.

Here's a simple test rig I have been using to inject an empty tag into vector's internal metrics stream and then attempt to clean it using compact.

### Configuration

```text
sources:
  demo:
    type: internal_metrics

transforms:
  dirty:
    type: remap
    inputs:
    - demo
    source: >
      .tags.empty = ""

  clean:
    type: remap
    inputs:
    - dirty
    source: |
      . = compact(.)

  m3l:
    type: metric_to_log
    inputs:
    - clean

sinks:
  cleanout:
    type: file
    inputs:
    - m3l
    path: /tmp/clean.json
    encoding:
      codec: json
      metrics_tag_values: full
```


### Version

0.28.1

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

https://github.com/vectordotdev/vrl/issues/186
