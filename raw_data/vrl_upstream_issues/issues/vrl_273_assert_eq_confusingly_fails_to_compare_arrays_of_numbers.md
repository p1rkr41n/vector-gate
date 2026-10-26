# [#273] assert_eq confusingly fails to compare arrays of numbers

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/273)
- **Status**: `OPEN`
- **Author**: [@jpeach](https://github.com/jpeach)
- **Created At**: `2023-03-23T00:26:53Z`
- **Updated At**: `2026-06-16T13:10:31Z`
- **Comments**: 2
- **Labels**: `vrl:stdlib`, `stdlib:assert_eq`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/273)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I have a test that looks like this:

```
    [[tests.outputs]]
    extract_from = "mangle"
    [[tests.outputs.conditions]]
    type = "vrl"
    source = '''
    wanted = {
        "date": "2023-03-22",
        "doc_id": "-",
        "tags_bools.key": ["is_provisioned"],
        "tags_bools.value": [true],
        "tags_exacts": [
            "input=syslog-journald",
            "is_provisioned=True",
            "message_size=110",
            "sequence_number=",
            "transport=journal",
        ],
        "tags_numbers.key": ["@version", "message_size"],
        "tags_numbers.value": [1, 110],
        "tags_strings.key": ["input", "sequence_number", "transport"],
        "tags_strings.value": ["syslog-journald", "",  "journal"],
        "timestamp": 1679504581104,
    }

    for_each(keys(.)) -> |_, k| {
        if k == "doc_id" {
            null
        } else {
            assert_eq!(get!(wanted, [k]), get!(., [k]))
        }
    }

    true
    '''
```

And the comparison fails:

```
  condition[0]: source execution failed:
error[E000]: function call error for "for_each" at (1198:1361): function call error for "assert_eq" at (1302:1345): assertion failed: [1, 110] == [1, 110]
   ┌─ :27:5
   │
27 │ ╭     for_each(keys(.)) -> |_, k| {
28 │ │         if k == "doc_id" {
29 │ │             null
30 │ │         } else {
31 │ │             assert_eq!(get!(wanted, [k]), get!(., [k]))
   │ │             ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^ assertion failed: [1, 110] == [1, 110]
32 │ │         }
33 │ │     }
   │ ╰─────^ function call error for "assert_eq" at (1302:1345): assertion failed: [1, 110] == [1, 110]
   │
   = see language documentation at https://vrl.dev
   = try your code in the VRL REPL, learn more at https://vrl.dev/examples

```

If I switch the wanted output to `"tags_numbers.value": [1.0, 110.0]`, then it succeeds.

### Configuration

_No response_

### Version

vector 0.28.1 (x86_64-apple-darwin ff15924 2023-03-06)

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
