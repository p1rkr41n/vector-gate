# [#15542] Delete root object changed behavior in 0.26.0 for vector test

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/15542)
- **Status**: `OPEN`
- **Author**: [@awangc](https://github.com/awangc)
- **Created At**: `2022-12-12T13:36:24Z`
- **Updated At**: `2026-02-21T20:39:09Z`
- **Comments**: 1
- **Labels**: `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/15542)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

In vector 0.25.2, the following test case passes:

```
[transforms.test]
  type = "remap"
  inputs = ["not_used"]
  source = '''
    .vector = del(.)
    .log.level = "warn"
  '''


[[tests]]
  name = "test_vector"

  [[tests.inputs]]
    insert_at = "test"
    type = "log"
    log_fields.message = "Received one event."

  [[tests.outputs]]
     extract_from = "test"

    [[tests.outputs.conditions]]
      type = "vrl"
      source = '''
        assert_eq!(.log.level, "warn", "log level failure")
        assert_eq!(.vector.message, "Received one event.", "message failure")
     '''
```
but in 0.26.0 it fails with following error message

```
❯ vector260 test test.toml
Running tests
2022-12-12T13:30:04.416094Z ERROR vector::unit_test: Failed to execute tests:
Failed to build test 'test_vector':
  Transform "test":
  error[E642]: parent path segment rejects this mutation
    ┌─ :2:10
    │
  2 │     .log.level = "warn"
    │     ---- ^^^^^ querying a field of a non-object type is unsupported
    │     │
    │     this path resolves to a value of type undefined
    │
    = try: change parent value to object, before assignment
    =
    =     .log = {}
    =     .log.level = "warn"
    =
    = see documentation about error handling at https://errors.vrl.dev/#handling
    = see language documentation at https://vrl.dev
    = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

### Configuration

```text
[transforms.test]
  type = "remap"
  inputs = ["not_used"]
  source = '''
    .vector = del(.)
    .log.level = "warn"
  '''


[[tests]]
  name = "test_vector"

  [[tests.inputs]]
    insert_at = "test"
    type = "log"
    log_fields.message = "Received one event."

  [[tests.outputs]]
     extract_from = "test"

    [[tests.outputs.conditions]]
      type = "vrl"
      source = '''
        assert_eq!(.log.level, "warn", "log level failure")
        assert_eq!(.vector.message, "Received one event.", "message failure")
     '''
```


### Version

vector 0.26.0 (x86_64-apple-darwin c6b5bc2 2022-12-05)

### Debug Output

```text
❯ RUST_BACKTRACE=full vector260 -vvv  test test.toml
2022-12-12T13:32:09.192628Z  INFO vector::app: Internal log rate limit configured. internal_log_rate_secs=10
Running tests
2022-12-12T13:32:09.196264Z DEBUG vector::topology::builder: Building new source. component=test-source-8a402a30-a0bf-4384-b6e7-4c05d78a69b1
2022-12-12T13:32:09.196709Z DEBUG vector::topology::builder: Building new transform. component=test
2022-12-12T13:32:09.196991Z DEBUG vector::topology::builder: Building new sink. component=test-sink-8a402a30-a0bf-4384-b6e7-4c05d78a69b1
2022-12-12T13:32:09.197161Z ERROR vector::unit_test: Failed to execute tests:
Failed to build test 'test_vector':
  Transform "test":
  error[E642]: parent path segment rejects this mutation
    ┌─ :2:10
    │
  2 │     .log.level = "warn"
    │     ---- ^^^^^ querying a field of a non-object type is unsupported
    │     │
    │     this path resolves to a value of type undefined
    │
    = try: change parent value to object, before assignment
    =
    =     .log = {}
    =     .log.level = "warn"
    =
    = see documentation about error handling at https://errors.vrl.dev/#handling
    = see language documentation at https://vrl.dev
    = try your code in the VRL REPL, learn more at https://vrl.dev/examples
  .
```


### Example Data

_No response_

### Additional Context

No reference to this behavior was made in the `breaking changes` upgrade guide of the release documentation https://vector.dev/highlights/2022-11-07-0-26-0-upgrade-guide/

### References

_No response_
