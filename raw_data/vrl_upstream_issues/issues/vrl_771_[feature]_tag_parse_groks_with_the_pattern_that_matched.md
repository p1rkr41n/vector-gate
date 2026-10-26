# [#771] [feature] tag parse_groks with the pattern that matched

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/771)
- **Status**: `OPEN`
- **Author**: [@ipsi](https://github.com/ipsi)
- **Created At**: `2024-03-27T16:12:26Z`
- **Updated At**: `2026-06-16T13:10:06Z`
- **Comments**: 1
- **Labels**: `vrl:stdlib`, `stdlib:parse_groks`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/771)

---

## Description

Per the [discussion on the Vector repo](https://github.com/vectordotdev/vector/discussions/20174), I would like it if VRL would tag the matching pattern, so that it's possible to, for example, route to different transformers or sinks based on which pattern was matched.

This is particularly relevant when hosting third-party software on Docker, for example, where you get might application logs mixed in with Apache Access & Error logs, and need to use something like Grok to detect the type and send to a different destination, or do post-processing on, for example.

I'm not sure what form this would take. For example, would a configuration like this:

```
parse_groks!(
	"2020-10-02T23:22:12.223222Z info Hello world",
	patterns: [
		"%{common_prefix} %{_status} %{_message}",
		"%{common_prefix} %{_message}",
	],
	aliases: {
		"common_prefix": "%{_timestamp} %{_loglevel}",
		"_timestamp": "%{TIMESTAMP_ISO8601:timestamp}",
		"_loglevel": "%{LOGLEVEL:level}",
		"_status": "%{POSINT:status}",
		"_message": "%{GREEDYDATA:message}"
	},
        tag_field: "grok_pattern"
)
```

Add the field `grok_pattern=%{common_prefix} %{_status} %{_message}` to the output, or `grok_pattern=0`, or would it be better to allow `patterns` to accept an object of named patterns, like so:

```
parse_groks!(
	"2020-10-02T23:22:12.223222Z info Hello world",
	patterns: {
		"status_pattern": "%{common_prefix} %{_status} %{_message}",
		"simple_pattern": "%{common_prefix} %{_message}",
	},
	aliases: {
		"common_prefix": "%{_timestamp} %{_loglevel}",
		"_timestamp": "%{TIMESTAMP_ISO8601:timestamp}",
		"_loglevel": "%{LOGLEVEL:level}",
		"_status": "%{POSINT:status}",
		"_message": "%{GREEDYDATA:message}"
	}
)
```

And (assuming VRL supports passing arrays OR objects like that), the output would automatically include `grok_pattern=status_pattern" if it's an object.
