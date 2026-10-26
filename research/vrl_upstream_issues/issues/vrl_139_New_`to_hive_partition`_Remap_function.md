# [#139] New `to_hive_partition` Remap function

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/139)
- **Status**: `OPEN`
- **Author**: [@binarylogic](https://github.com/binarylogic)
- **Created At**: `2021-01-15T18:37:20Z`
- **Updated At**: `2026-06-01T14:16:12Z`
- **Comments**: 6
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/139)

---

## Description

Creating Hive partition strings is very common when writing to file-like storages (such as `aws_s3`). Unfortunately, creating these partition strings is fraught with foot-guns. To protect users from these issues we should offer a function that makes this task easy.

## Examples

Given this event for all examples:

```json
{
	"timestamp": "2021-01-14T21:26:45.433667Z",
	"application_id": 2,
	"environment": "production"
}
```

### Array

And this Remap script:

```js
to_hive_partition([.environment, .application_id, .timestamp], limit: 256)
```

Would produce this string:

```
environment=production/application_id=2/timestamp_year=2020/timestamp_month=01/timestamp_day=14/
```

Notice that:

1. The keys reflect the path names (curious if this is possible)
2. The timestamp is opinionated: truncated by the day and split into 3 partitions

### Map

And this Remap script:

```js
to_hive_partition({"env": .environment, "app": .application_id, "ts": .timestamp}, limit: 256)
```

Would produce this string:

```
env=production/app=2/ts_year=2020/ts_month=01/ts_day=14/
```

Notice that the map keys are used as the names

### Single value

And this Remap script:

```js
to_hive_partition(.timestamp, limit: 256)
```

Would produce this string:

```
timestamp_year=2020/timestamp_month=01/timestamp_day=14/
```

## Requirements

- [ ] Key/value pairs should be delimited by `/`
- [ ] Keys and values should be delimited by `=`
- [ ] Keys _and_ values must be URL encoded as to not conflict with the reserved characters above.
- [ ] The overall partition length cannot exceed 256 characters for most use cases.
- [ ] Opinionated formatted of timestamps.
- [ ] Includes a trailing `/` character

cc @jszwedko since he had the pleasure of creating such partition strings for the benchmarking work.
