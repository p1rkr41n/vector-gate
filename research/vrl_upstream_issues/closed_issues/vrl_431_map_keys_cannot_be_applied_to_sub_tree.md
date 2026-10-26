# Issue #431: `map_keys` cannot be applied to sub tree

- **URL:** https://github.com/vectordotdev/vrl/issues/431
- **Author:** @nettnikl
- **Status:** CLOSED (completed)
- **Created:** 2023-08-31T16:32:05Z
- **Closed:** 2023-09-01T15:17:11Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

`map_keys` seems not to be able to be used on sub trees only. Am i misunderstanding the docs or misdoing the config?

### Configuration

```text
[transforms.docker_logs]
type = "remap"
inputs = [ "docker" ]
source = """
. = map_keys(.labels, recursive: true) -> |key| { replace(key, ".", "_") }
"""
```


### Version

0.32.1

### Debug Output

```text
vector  | 2023-08-31T16:29:43.972767Z ERROR vector::topology: Configuration error. error=Transform "docker_logs2": 
vector  | error[E121]: type mismatch in closure parameter
vector  |   ┌─ :2:5
vector  |   │
vector  | 2 │ . = map_keys(.labels, recursive: true) -> |key| { replace(key, ".", "_") }
vector  |   │     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
vector  |   │     │
vector  |   │     the closure tied to this function call expects a different input value
vector  |   │     expression has an inferred type of any where an array or object was expected
vector  |   │
vector  |   = see language documentation at https://vrl.dev
vector  |   = try your code in the VRL REPL, learn more at https://vrl.dev/examples
vector  | 
vector exited with code 0
```


### Example Data

_No response_

### Additional Context

vector in docker

### References

_No response_
