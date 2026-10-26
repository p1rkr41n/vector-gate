# [#503] Add formats parameter to parse_timestamp

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/503)
- **Status**: `OPEN`
- **Author**: [@mattnthat](https://github.com/mattnthat)
- **Created At**: `2023-10-10T23:56:26Z`
- **Updated At**: `2026-06-16T13:10:16Z`
- **Comments**: 2
- **Labels**: `vrl:stdlib`, `stdlib:parse_timestamp`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/503)

---

## Description



As per conversation on [this thread](https://github.com/vectordotdev/vrl/issues/189#issuecomment-1755753131)

With the removal of the `to_timestamp` function, it's become harder to handle / normalise unknown timestamps in input data.

The feature as suggested by @jszwedko is to extend `parse_timestamp` to accept a 'format' parameter which can be an array of timestamp formats to try to match.
This puts control of the timestamp format array onto the user (vector.dev team don't have to hardcode and constantly extend acceptable formats) but gives the user a simple way to match a wide variery of timestamp formats in the incoming data.

Work around suggested in the comment thread above gives some good structure around how the feature could work:

```
formats = ["%+c", "some other format"]
t1 = now() # default
for_each(formats) -> |_index, format| {
  t2, err = parse_timestamp(.timestamp, "some other format")
  if err == null {
    t1 = t2
  }
}
.timestamp = t1
```



