# [#790] parse_timestamp Invalid timestamp error

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/790)
- **Status**: `OPEN`
- **Author**: [@DimDroll](https://github.com/DimDroll)
- **Created At**: `2024-04-10T02:21:27Z`
- **Updated At**: `2026-06-16T13:10:04Z`
- **Comments**: 4
- **Labels**: `vrl:stdlib`, `stdlib:parse_timestamp`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/790)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Hello,

We have a case when we need to parse nanoseconds timestamp like 1712312062676735437 using parse_timestamp function:
`.2_timestamp = parse_timestamp!("1712312062676735437", "%s%f")`
Which gives error:
```
error[E000]: function call error for "parse_timestamp" at (152:199): Invalid timestamp "1712312062676735437": premature end of input
  ┌─ :5:16
  │
5 │ .2_timestamp = parse_timestamp!("1712312062676735437", "%s%f")
  │                ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ Invalid timestamp "1712312062676735437": premature end of input
  │
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

The workaround is to add space in between timestamp and nanoseconds part:
`.4_timestamp = parse_timestamp!("1712312062 676735437", "%s %f")`

Following is VRL code that can be executed in [playground](https://playground.vrl.dev/):
```
Vector Version:	5ffb1a55
VRL Version:	0.13.0
```
I assume same happens during real-time run.

```
# does not parse nanoseconds timestamp
# error: premature end of input
#.1_timestamp = parse_timestamp!("1712312062676735437", "%s%9f")
#.2_timestamp = parse_timestamp!("1712312062676735437", "%s%f")

# does parse
# by adding space in-between
# unix timestamp and nanoseconds
.3_timestamp = parse_timestamp!("1712312062 676735437", "%s %9f")
.4_timestamp = parse_timestamp!("1712312062 676735437", "%s %f")

# workaround
full_timestamp = "1712312062676735437"
timestamp_slice = slice!(full_timestamp, 0, 10)
nanoseconds_slice = slice!(full_timestamp, 10)
.5_timestamp = parse_timestamp!(timestamp_slice + " " + nanoseconds_slice, "%s %f")

# another obeservation
# following results in strange concatenation error
# error: trailing input
#.6_timestamp = parse_timestamp!("1712312062" + " ", "%s ")
# but following works fine:
#.7_timestamp = parse_timestamp!("1712312062" + " A", "%s A")

# dirty workaround
#full_timestamp = "1712312062676735437"
#timestamp_slice = slice!(full_timestamp, 0, 10)
#nanoseconds_slice = slice!(full_timestamp, 10)
# parse timestamp and add nanoseconds post-factum
#.8_timestamp = parse_timestamp!(timestamp_slice, "%s")
#.8_timestamp = replace(to_string(.9_timestamp), "Z", "." + nanoseconds_slice + "Z")
```



### Configuration

_No response_

### Version

VRL Version:	0.13.0

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
