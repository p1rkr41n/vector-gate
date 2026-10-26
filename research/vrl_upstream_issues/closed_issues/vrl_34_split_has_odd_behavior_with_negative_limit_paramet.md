# Issue #34: `split` has odd behavior with negative `limit` parameter

- **URL:** https://github.com/vectordotdev/vrl/issues/34
- **Author:** @briankung
- **Status:** CLOSED (completed)
- **Created:** 2022-08-09T03:31:12Z
- **Closed:** 2023-03-29T03:50:00Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

## Expected behavior

vrl returns an error.

## Actual behavior

`split` treats `limit` as `usize::MAX` 

```
$ split("This is a long string", " ",  -10000)
["This", "is", "a", "long", "string"]
```

## Notes

The behavior is due to [this cast](https://github.com/vectordotdev/vector/blob/master/lib/vrl/stdlib/src/split.rs#L6): 

```rust
let limit = limit.try_integer()? as usize;
```
See playground link here: https://play.rust-lang.org/?version=stable&mode=debug&edition=2021&gist=e33b58675012c83493efef2dbb9aa920

```rust
let number = -1_i64 as usize;
dbg!((number, number == usize::MAX));

// [src/main.rs:3] (number, number == usize::MAX) = (
//    18446744073709551615,
//    true,
//)
```

### Version

vector 0.24.0 (x86_64-apple-darwin debug=full)
