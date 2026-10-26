# Issue #5246: remap-lang: improve arithmetic type checking and test coverage

- **URL:** https://github.com/vectordotdev/vector/issues/5246
- **Author:** @JeanMertz
- **Status:** CLOSED (completed)
- **Created:** 2020-11-26T17:09:38Z
- **Closed:** 2021-02-15T15:40:15Z
- **Labels:** domain:reliability, domain:vrl

## Description

In #5059 we've improved type checking of arithmetic operations to be more exact than before. However, as @FungusHumungus notes in https://github.com/timberio/vector/pull/5059#discussion_r524445777, there is still more we can do to get more precise type information.

For example, `"foo" * 3` is valid, and will always return `"foofoofoo"`, but the type definition of this expression resolves to `Bytes | Integer | Float`, which isn't wrong, but also isn't as accurate as it can be (e.g. `Bytes`).

Additionally, we need to expand our test coverage of the arithmetic expression logic, as there are still some gaps in its functionality.

For example, while `"foo" * 3` works, `3 * "foo"` does not.
