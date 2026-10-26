# Issue #1107: to_float and infinity result can crash vector

- **URL:** https://github.com/vectordotdev/vrl/issues/1107
- **Author:** @dhable
- **Status:** CLOSED (completed)
- **Created:** 2024-11-01T14:53:06Z
- **Closed:** 2024-12-11T15:03:14Z
- **Labels:** None

## Description

We ran into an issue where parsing a string with `to_float` exceeds the bounds of `f64::MAX`, which returns a non-error infinity value.
```
$ str_value = "61687855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562"
"61687855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562"

$ parsed_value, err = to_float(str_value)
inf

$ err
null
```
Since `err` was `null`, it's might seem like it's safe to perform operations on this value but subtraction causes vector to panic and crash. This is because `f64::INFINITY - f64::INFINITY == f64::NAN` in rust.
```
$ parsed_value + parsed_value
inf

$ parsed_value + 1
inf

$ parsed_value - 1
inf

$ 1 - parsed_value
-inf

$ parsed_value - parsed_value
thread 'main' panicked at /Users/dan.hable/.cargo/registry/src/index.crates.io-6f17d22bba15001f/ordered-float-4.2.2/src/lib.rs:1331:37:
Subtraction resulted in NaN: FloatIsNan
note: run with `RUST_BACKTRACE=1` environment variable to display a backtrace
```
I can't find anything in the VRL language, besides using `to_string` to compare with "inf", that would allow me to detect this situation and avoid operations on infinite values. IMHO, I would have expected an error result instead of infinity, similar to how `to_int` behaves.
```
$ parsed_value, err = to_int(str_value)
"function call error for \"to_int\" at (20:29): Invalid integer \"61687855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562855628556285562\": number too large to fit in target type"
``` 
