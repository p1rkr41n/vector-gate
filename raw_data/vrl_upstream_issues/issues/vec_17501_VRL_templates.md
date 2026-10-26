# [#17501] VRL templates

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/17501)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2023-05-26T15:06:20Z`
- **Updated At**: `2026-05-29T23:44:58Z`
- **Comments**: 2
- **Labels**: `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/17501)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Proposal

Today templates are very limited, they can only contain the following:
- A literal string
- A literal string with a timestamp
- A reference to a single event field

It would be nice to allow the full power of VRL to calculate template values. For example, a field reference in a template today will generally return an error if the field is missing. In VRL, it could choose an arbitrary default.

VRL supports read-only mode (currently used in VRL conditions), which can prevent mutations. This was one of the issues in the previous RFC.

It can also (with a [minor](https://github.com/vectordotdev/vrl/issues/240) change) type check the result of the VRL template to ensure it always returns a string.

Some sinks (such as `Loki`) allow deleting fields after they are referenced in a template. I suggest that VRL templates are immutable and never modify the event, they only can calculate and return a new value. If there is data that should be used in a template, but _not_ sent to the sink, it should be moved into event metadata first (in a `remap` transform).

Since the templating logic is very limited today, this can probably be made fully backwards compatible, so either a "legacy" template, or a VRL script can be used in a template. Internally all templates will be converted to a VRL script. A warning could even be generated if the "legacy" templates are being used, with the VRL code that it can be converted to.


Previous RFC: https://github.com/vectordotdev/vector/pull/4905
