# [#1543] `parse_timestamp()` function does not honnor all chrono's strftime() tokens (specifically the `%z` token)

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1543)
- **Status**: `OPEN`
- **Author**: [@kquinsland01](https://github.com/kquinsland01)
- **Created At**: `2025-10-23T00:41:08Z`
- **Updated At**: `2026-06-01T14:08:45Z`
- **Comments**: 0
- **Labels**: `stdlib:parse_timestamp`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1543)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

This was originally issue [#24049](https://github.com/vectordotdev/vector/issues/24049) but it wasn't until a few hours after opening that when i discovered that the `vrl` sub-component was it's own repo.
The bug - as best as I can tell - belongs here and **not** on the core `vector` repo.

---


It's taken me a while to narrow it down to the minimal reproducible example, but here's a [playground link](https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiIyAxNzYxMDgyMDc2ID0gVHVlc2RheSwgT2N0b2JlciAyMSwgMjAyNSA5OjI3OjU2IFBNIGluIEdNVFxuIyBUaGF0IHRpbWUsIHBsdXMgMmgzMG0gd291bGQgYmUgMTE6NTcgUE1cbiMjXG4jIERvY3Mgc2F5IHRoYXQgJXMgaXMgdW5peCBlcG9jaCBzZWNvbmRzIGFuZCAleiBpcyB0aGUgK0hITU0gZm9ybWF0XG4jIFRoZSAleiMgdmFyIGFsbG93cyBtaW4gdG8gYmUgb3B0aW9uYWxcbiMgU2VlOiBodHRwczovL2RvY3MucnMvY2hyb25vL2xhdGVzdC9jaHJvbm8vZm9ybWF0L3N0cmZ0aW1lL2luZGV4Lmh0bWwjc3BlY2lmaWVyc1xuIyNcbi5leHBlY3RfZHQ9XCIyMDI1LTEwLTIxVDIzOjU3OjU2WlwiXG4ucGFyc2VkX2R0LCAudHNfZXBvY2hfc3RyaW5nX3BhcnNlX2VyciA9IHBhcnNlX3RpbWVzdGFtcCh2YWx1ZTogXCIxNzYxMDgyMDc2KzAyMzBcIiwgZm9ybWF0OiBcIiVzJSN6XCIpXG4iLCJldmVudCI6e30sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9):

And if you want to inspect / copy/paste manually, first:

```
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiIyAxNzYxMDgyMDc2ID0gVHVlc2RheSwgT2N0b2JlciAyMSwgMjAyNSA5OjI3OjU2IFBNIGluIEdNVFxuIyBUaGF0IHRpbWUsIHBsdXMgMmgzMG0gd291bGQgYmUgMTE6NTcgUE1cbiMjXG4jIERvY3Mgc2F5IHRoYXQgJXMgaXMgdW5peCBlcG9jaCBzZWNvbmRzIGFuZCAleiBpcyB0aGUgK0hITU0gZm9ybWF0XG4jIFRoZSAleiMgdmFyIGFsbG93cyBtaW4gdG8gYmUgb3B0aW9uYWxcbiMgU2VlOiBodHRwczovL2RvY3MucnMvY2hyb25vL2xhdGVzdC9jaHJvbm8vZm9ybWF0L3N0cmZ0aW1lL2luZGV4Lmh0bWwjc3BlY2lmaWVyc1xuIyNcbi5leHBlY3RfZHQ9XCIyMDI1LTEwLTIxVDIzOjU3OjU2WlwiXG4ucGFyc2VkX2R0LCAudHNfZXBvY2hfc3RyaW5nX3BhcnNlX2VyciA9IHBhcnNlX3RpbWVzdGFtcCh2YWx1ZTogXCIxNzYxMDgyMDc2KzAyMzBcIiwgZm9ybWF0OiBcIiVzJSN6XCIpXG4iLCJldmVudCI6e30sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9
``` 


If that link ever dies, here's the `.vrl`:

```vrl
# 1761082076 = Tuesday, October 21, 2025 9:27:56 PM in GMT
# That time, plus 2h30m would be 11:57 PM
##
# Docs say that %s is unix epoch seconds and %z is the +HHMM format
# The %z# var allows min to be optional
# See: https://docs.rs/chrono/latest/chrono/format/strftime/index.html#specifiers
##
.expect_dt="2025-10-21T23:57:56Z"
.parsed_dt, .ts_epoch_string_parse_err = parse_timestamp(value: "1761082076+0230", format: "%s%#z")
```

The `input`: 

```json
{}
```

And _critically_ the `output`:

```json
{
	"expect_dt": "2025-10-21T23:57:56Z",
	"parsed_dt": "2025-10-21T21:27:56Z",
	"ts_epoch_string_parse_err": null
}
```

Note that the provided string: `1761082076+0230` **should** have returned `2025-10-21T23:57:56Z` but instead I got the timestamp that is 2h30m early: `2025-10-21T21:27:56Z`

**I can also reproduce this locally**
At first, I thought that this may have been a bug(?) with the web tool but the same results are present when doing things locally:

```shell
# Check version; it's new
❯ vector --version
vector 0.50.0 (aarch64-apple-darwin 9053198 2025-09-23 14:18:50.944442940)

# Show that it's the same program used on web
❯ /bin/cat poc.vrl
# 1761082076 = Tuesday, October 21, 2025 9:27:56 PM in GMT
# That time, plus 2h30m would be 11:57 PM
##
# Docs say that %s is unix epoch seconds and %z is the +HHMM format
# The %z# var allows min to be optional
# See: https://docs.rs/chrono/latest/chrono/format/strftime/index.html#specifiers
##
.expect_dt="2025-10-21T23:57:56Z"
.parsed_dt, .ts_epoch_string_parse_err = parse_timestamp(value: "1761082076+0230", format: "%s%#z")

# The vrl function won't do anything unless there's input so create a dummy input
❯ /bin/cat poc.json
{"empty": "event"}

# And then run with max logging
❯ RUST_BACKTRACE=full vector -vvv  vrl --input=poc.json --program=poc.vrl --print-object
2025-10-22T18:29:59.031245Z DEBUG vector::app: Internal log rate limit configured. internal_log_rate_secs=10
2025-10-22T18:29:59.031272Z  INFO vector::app: Log level is enabled. level="trace"
2025-10-22T18:29:59.031282Z DEBUG vector::app: messaged="Building runtime." worker_threads=11
2025-10-22T18:29:59.031323Z TRACE mio::poll: registering event source with poller: token=Token(1), interests=READABLE
{ "empty": "event", "expect_dt": "2025-10-21T23:57:56Z", "parsed_dt": t'2025-10-21T21:27:56Z', "ts_epoch_string_parse_err": null }
```

### VRL Program

```text
(see above)
```

### VRL and/or Vector Version

vector 0.50.0 (aarch64-apple-darwin 9053198 2025-09-23 14:18:50.944442940)

### Debug Output

```text

```

### Example

(see above)

### Additional Context

And just as a sanity check, I hacked up a very crude test in rust:

```rust
use chrono::DateTime;

fn main() {
    // 1761082076 = Tuesday, October 21, 2025 9:27:56 PM in GMT
    let raw_epoch_str = "1761082076";
    let epoch_offset_str = "+0230";
    println!("Epoch: {}", raw_epoch_str);
    println!("Offset: {}", epoch_offset_str);

    let expected_datetime = chrono::NaiveDateTime::from_timestamp(
        raw_epoch_str.parse::<i64>().unwrap(),
        0,
    );
    println!("Epoch, parsed: {}", expected_datetime);

    let epoch_string = format!("{}{}", raw_epoch_str, epoch_offset_str);
    println!("Offset Epoch String: {}", epoch_string);
    let format_str = "%s%z";

    let parsed_datetime = DateTime::parse_from_str(&epoch_string, format_str).unwrap();
    println!("Parsed Epoch String: {}", parsed_datetime);

}
```

This is with:

```shell
❯ /bin/cat Cargo.toml
[package]
name = "crono-test"
version = "0.1.0"
edition = "2024"

[dependencies]
chrono = "0.4.42"
```

And the results match what I would expect vector to do:

```shell
❯ cargo run
   Compiling crono-test v0.1.0 (/Users/karl.quinsland/Downloads/crono-test)
warning: use of deprecated associated function `chrono::NaiveDateTime::from_timestamp`: use `DateTime::from_timestamp` instead
  --> src/main.rs:10:52
   |
10 |     let expected_datetime = chrono::NaiveDateTime::from_timestamp(
   |                                                    ^^^^^^^^^^^^^^
   |
   = note: `#[warn(deprecated)]` on by default

warning: `crono-test` (bin "crono-test") generated 1 warning
    Finished `dev` profile [unoptimized + debuginfo] target(s) in 0.14s
     Running `target/debug/crono-test`
Epoch: 1761082076
Offset: +0230
Epoch, parsed: 2025-10-21 21:27:56
Offset Epoch String: 1761082076+0230
Parsed Epoch String: 2025-10-21 23:57:56 +02:30
```

### References

_No response_
