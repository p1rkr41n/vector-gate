# [#4] Reduce boilerplate required to add VRL parsing functions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/4)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2023-02-17T18:02:45Z`
- **Updated At**: `2023-04-10T14:46:57Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/4)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Goals:
- Be able to define a new VRL parsing function by only supplying the following: 
   - A function name
   - A parsing implementation (nom / grok / regex / etc)
   - A VRL type definition
   - Examples
- The following boilerplate should _not_ be required:
   - The vrl `resolve`, `compile`, and `parameters` are not needed
   - maybe remove the need to feature flag each individual parser
- Re-write existing functions with the _new_ method.

Non-Goals:
- at least initially, parsers that require inputs other than `value` (the string being parsed) are out of scope


