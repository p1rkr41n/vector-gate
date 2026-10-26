# Issue #1353: Should is_nullish([]) and is_nullish({}) return true?

- **URL:** https://github.com/vectordotdev/vrl/issues/1353
- **Author:** @nf-brentsaner
- **Status:** CLOSED (completed)
- **Created:** 2025-03-22T21:34:11Z
- **Closed:** 2025-03-31T15:26:46Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->

Currently, `is_nullish([])` and `is_nullish({})` will return `false`.

Now, there is of course `is_empty()`, but there's also `is_null()`. There are many cases where one is not only just concerned with "populated" strings, but also "populated" arrays and maps/objects without knowing what explicit type it is.

Per the documentation for `is_nullish()`:

> Determines whether value is nullish, where nullish denotes the *absence of a meaningful value*.

_(emphasis added)_

IMHO `is_nullish([])` and `is_nullish({})` should return `true` to be consistent with/parallel to the pattern/behavior/relation/intent of `is_empty("")` ↔ `is_nullish("")`, and more in line with the stated design intent of `is_nullish()`.

This is/would be, of course, unfortunately a breaking change but it is arguably a more "correct" implementation.

### Use Cases

Given the following data:

<details>
<summary>`data.json`</summary>

```json
{"log":{"items":[{"foo":null},{"foo":""},{"foo":[]},{"foo":{}},{"foo":"something happened"},{"foo":["a thing happened","then another thing happened"]},{"foo":{"thing1":"happened!","thing2":"did not happen, shucks"}}]}}
```

Exploded/"pretty", for convenience on human eyes/to save you the `jq` trip:
```json
{
  "log": {
    "items": [
      {
        "foo": null
      },
      {
        "foo": ""
      },
      {
        "foo": []
      },
      {
        "foo": {}
      },
      {
        "foo": "something happened"
      },
      {
        "foo": [
          "a thing happened",
          "then another thing happened"
        ]
      },
      {
        "foo": {
          "thing1": "happened!",
          "thing2": "did not happen, shucks"
        }
      }
    ]
  }
}

_(As an aside, any chance of getting `vector vrl` working with the exploded/"pretty" form of JSON input? Want a separate issue for that or does one already exist?)_
```

</details>

The following VRL program will *not* do what one would think it does based on the description of `is_nullish()` (liberal use of `log()` instead of `assert()` to make sure all cases are demonstrated without abort):

<details>
<summary>`test.vrl`</summary>

```
log("BEGIN")

items = array!(.log.items)

for_each(items) -> |idx, item| {

  val = item.foo

  path_str = ".log.items.[" + to_string(idx) + "].foo"

  log_ins_str = " "
  target = false
  if idx < 4 {
    log_ins_str = " no "
    target = true
  }

  evald = is_nullish(val)

  n = evald == target

  log(
	"\n
	Path " + path_str + " has" + log_ins_str + "meaningful data.
	Value: " + encode_json(val, false) + "
	Target: " + to_string(target) + "
	Evaluated: " + to_string(evald) + "
	Confirmed: " + to_string(n) + "
	\n",
  rate_limit_secs: 0
  )
}

log("END")
```

</details>

### Attempted Solutions

The only alternative currently for an *accurate* and *correct* evaluation of whether an array or map/object has meaningful data is to first check:

```
if (is_array(item) || is_object(item)) && is_empty(item) { ... }`
```

which is kind of a PITA, especially if the value can ALSO be a string, which **then** becomes:

```
if (is_array(item) || is_object(item) || is_string(item)) && is_empty(item) { ... }
```

or

```
if ((is_array(item) || is_object(item) && is_empty(item)) || (is_string(item) && is_nullish(item)) { ... }
```

instead of just:

```
if is_nullish(item) { ... }
```

for all three types.

### Proposal

As stated above, `is_nullish([])` and `is_nullish({})` should return `true` instead of `false`.

### References

_No response_
