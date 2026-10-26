# [#23651] Incomplete support for changing time zones

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/23651)
- **Status**: `OPEN`
- **Author**: [@piotrminkina](https://github.com/piotrminkina)
- **Created At**: `2025-08-26T13:52:08Z`
- **Updated At**: `2026-05-29T23:27:08Z`
- **Comments**: 0
- **Labels**: `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/23651)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->

### Problem

I am not sure if this is strictly a VRL problem or perhaps a Vector problem. It seems that the handling of changing time zones, such as in the _Europe/Warsaw_ zone, where there is a +2h shift relative to UTC during summer time and a +1h shift during winter time, is not entirely correct. The problem becomes apparent in tests when parsing dates from a different zone than the one in effect at the time. For example, I parse a date in CET when CEST is in effect. I am providing a complete example with tests where this problem occurs.

Incidentally, I noticed that this special pattern using Datadog matchers does not work with the `parse_grok()` function.

### Configuration

```text
---
timezone: 'Europe/Warsaw'

transforms:
  parse_date:
    type: remap
    inputs: []
    source: |
      # Why doesn't parse_grok() support this pattern format, but parse_grok() does?
      . = parse_groks!(
        .message,
        [
          s'%{date("dd/MMM/yyyy:HH:mm:ss.SSS","Europe/Warsaw"):parsed_date}'
        ]
      )
      .parsed_date = from_unix_timestamp!(.parsed_date, unit: s'milliseconds')

tests:
  - name: check proper support for CET timezone
    inputs:
      - insert_at: parse_date
        type: log
        log_fields:
          # CET (+1 hour)
          message: '02/Jan/2000:03:04:05.006'
    outputs:
      - extract_from: parse_date
        conditions:
          - type: vrl
            source: |
              assert_eq!(.parsed_date, t'2000-01-02T02:04:05.006Z')

  - name: check proper support for CEST timezone
    inputs:
      - insert_at: parse_date
        type: log
        log_fields:
          # CEST (+2 hours)
          message: '13/Aug/2025:12:00:00.123'
    outputs:
      - extract_from: parse_date
        conditions:
          - type: vrl
            source: |
              assert_eq!(.parsed_date, t'2025-08-13T10:00:00.123Z')
```

### Version

vector 0.49.0 (x86_64-unknown-linux-gnu dc7e792 2025-08-12 13:47:08.632326804)

### Debug Output

```text
Running tests
test check proper support for CET timezone ... failed
test check proper support for CEST timezone ... passed

failures:

test check proper support for CET timezone:

check[0] for transforms ["parse_date"] failed conditions:

  condition[0]: source execution failed: 
error[E000]: function call error for "assert_eq" at (0:53): assertion failed: t'2000-01-02T01:04:05.006Z' == t'2000-01-02T02:04:05.006Z'
  ┌─ :1:1
  │
1 │ assert_eq!(.parsed_date, t'2000-01-02T02:04:05.006Z')
  │ ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ assertion failed: t'2000-01-02T01:04:05.006Z' == t'2000-01-02T02:04:05.006Z'
  │
  = see language documentation at https://vrl.dev
  = try your code in the VRL REPL, learn more at https://vrl.dev/examples


output payloads from ["parse_date"] (events encoded as JSON):
  {"parsed_date":"2000-01-02T01:04:05.006Z"}

```

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
