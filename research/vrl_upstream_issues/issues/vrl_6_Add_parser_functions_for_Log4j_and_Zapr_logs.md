# [#6] Add parser functions for Log4j and Zapr logs

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/6)
- **Status**: `OPEN`
- **Author**: [@AnkkeetVaity27](https://github.com/AnkkeetVaity27)
- **Created At**: `2023-01-13T09:17:58Z`
- **Updated At**: `2026-06-01T14:17:35Z`
- **Comments**: 2
- **Labels**: `vrl:stdlib`, `good first issue`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/6)

---

## Description

Currently we are using following Regex functions for parsing Log4j and Zapr logs:

`parse_log4j, err = parse_regex(.raw_message, r'(?s)\A(?P<level>[A-Z]+) *\[(?P<thread_type>[^-.:#(\]]+)[-.:#]?(?P<thread_id>[^\]]*)\] (?P<timestamp>.{10} .{12}) *(?P<source_file>[^:]+):(?P<source_line>\d+) - *(?P<message>.*)')`

`parse_zapr, err = parse_regex(.raw_message, r'(?s)(?P<timestamp>[\d-]+T[\d:.]+Z)\s+(?P<level>[A-Z]+)\s+(?P<source_file>[\w.]+)\s+(?P<message>.*)')`

It would be great to have parser functions for these log types.
