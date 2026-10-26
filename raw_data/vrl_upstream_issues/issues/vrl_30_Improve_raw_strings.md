# [#30] Improve raw strings

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/30)
- **Status**: `OPEN`
- **Author**: [@fuchsnj](https://github.com/fuchsnj)
- **Created At**: `2022-08-24T14:08:36Z`
- **Updated At**: `2023-03-28T13:15:58Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:parser`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/30)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Today the backslash (`\`) behavior inside raw strings can be confusing / inconsistent. The [docs](https://master.vector.dev/docs/reference/vrl/expressions/#string) claim that backslashes have "no special meaning", however a backslash currently causes the parser to always include the next character (_including_ the backslash itself). That means a blackslash can be used to include a single quote inside of a raw string, but this comes with some odd edge cases:

1. A single quote can't be included in a raw string without a leading backslash
2. The last character of a raw string cannot be a backslash

It would be nice if these restrictions could be lifted and a backslash actually had no special meaning.


### Proposal

One possible solution is to allow raw string literals similar to Rust, where you can create a custom delimiter out of multiple characters, which would allow anything to be used inside of the raw string literal.


### Version

0.23.0
