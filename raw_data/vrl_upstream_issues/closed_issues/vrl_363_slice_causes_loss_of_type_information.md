# Issue #363: `slice` causes loss of type information 

- **URL:** https://github.com/vectordotdev/vrl/issues/363
- **Author:** @apollo13
- **Status:** CLOSED (completed)
- **Created:** 2023-01-26T12:59:09Z
- **Closed:** 2025-02-05T19:13:28Z
- **Labels:** meta:confirmed

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I am upgrading an old vector instance to 0.27 and VRL code started breaking apart. The breakage starts with 0.24:
```
2023-01-26T12:55:08.211906Z ERROR vector::unit_test: Failed to execute tests:
Failed to build test 'udp ipv4 block':
  Transform "filterlog": 
  error[E620]: can't abort infallible function
     ┌─ :10:10
     │
  10 │   "ttl": to_int!(csv[2]),
     │          ^^^^^^- remove this abort-instruction
     │          │
     │          this function can't fail
     │
     = see documentation about error handling at https://errors.vrl.dev/#handling
     = see language documentation at https://vrl.dev
     = try your code in the VRL REPL, learn more at https://vrl.dev/examples
  ```

The `to_int` function is documented as `fallible`, so why do I get an error about it being infallible? Do I miss something obvious?

### Configuration

```text
---

transforms:
  filterlog:
    type: remap
    inputs:
      - syslog
    source: |
      if .appname != "filterlog" {
        abort
      }
      csv = parse_csv!(.message)
      log = {
        "rule_number": to_int!(csv[0]),
      }
      csv = slice!(csv, 9)
      log |= {
        "ttl": to_int(csv[2]),
      }
      .message = log
  filterlog-encoded:
    type: remap
    inputs:
      - filterlog
    source: .message = encode_logfmt!(.message, ["action", "real_interface", "direction", "source_address", "destination_address"])

tests:
  - name: udp ipv4 block
    inputs:
      - insert_at: filterlog
        type: log
        log_fields:
          message: 8,,,1000000103,igb0.100,match,block,in,4,0x0,,64,42660,0,DF,17,udp,51,192.168.100.10,225.0.0.1,44800,6666,31
          appname: filterlog

    outputs:
      - conditions:
          - .message.rule_number == 8
        extract_from: filterlog

  - name: tcp ipv4 block
    inputs:
      - insert_at: filterlog
        type: log
        log_fields:
          message: 8,,,1000000103,igb1,match,block,in,4,0x0,,64,57098,0,DF,6,tcp,72,33.188.11.129,12.188.11.131,33883,80,0,S,1307383639,,29200,,mss;sackOK;TS;nop;wscale;
          appname: filterlog

    outputs:
      - conditions:
          - .message.rule_number == 8
        extract_from: filterlog
```


### Version

0.27.0

### Debug Output

```text
2023-01-26T12:58:41.930489Z  INFO vector::app: Internal log rate limit configured. internal_log_rate_secs=10
Running tests
2023-01-26T12:58:41.933216Z DEBUG vector::topology::builder: Building new source. component=filterlog-source-d9a32171-07a5-408a-b842-d50ee14d4d57
2023-01-26T12:58:41.933586Z DEBUG vector::topology::builder: Building new transform. component=filterlog
2023-01-26T12:58:41.934033Z DEBUG vector::topology::builder: Building new sink. component=filterlog-sink-d9a32171-07a5-408a-b842-d50ee14d4d57
2023-01-26T12:58:41.935916Z DEBUG vector::topology::builder: Building new source. component=filterlog-source-d9a32171-07a5-408a-b842-d50ee14d4d57
2023-01-26T12:58:41.935967Z DEBUG vector::topology::builder: Building new transform. component=filterlog
2023-01-26T12:58:41.936417Z DEBUG vector::topology::builder: Building new sink. component=filterlog-sink-d9a32171-07a5-408a-b842-d50ee14d4d57
2023-01-26T12:58:41.936468Z ERROR vector::unit_test: Failed to execute tests:
Failed to build test 'udp ipv4 block':
  Transform "filterlog": 
  error[E620]: can't abort infallible function
     ┌─ :10:10
     │
  10 │   "ttl": to_int!(csv[2]),
     │          ^^^^^^- remove this abort-instruction
     │          │
     │          this function can't fail
     │
     = see documentation about error handling at https://errors.vrl.dev/#handling
     = see language documentation at https://vrl.dev
     = try your code in the VRL REPL, learn more at https://vrl.dev/examples
  
Failed to build test 'tcp ipv4 block':
  Transform "filterlog": 
  error[E620]: can't abort infallible function
     ┌─ :10:10
     │
  10 │   "ttl": to_int!(csv[2]),
     │          ^^^^^^- remove this abort-instruction
     │          │
     │          this function can't fail
     │
     = see documentation about error handling at https://errors.vrl.dev/#handling
     = see language documentation at https://vrl.dev
     = try your code in the VRL REPL, learn more at https://vrl.dev/examples
  .
```


### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
