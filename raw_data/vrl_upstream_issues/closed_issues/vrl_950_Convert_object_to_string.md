# Issue #950: Convert object to string.

- **URL:** https://github.com/vectordotdev/vrl/issues/950
- **Author:** @evanzhang87
- **Status:** CLOSED (completed)
- **Created:** 2024-07-22T04:06:34Z
- **Closed:** 2024-07-25T12:29:47Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

```
{
    "key_l1": "value",
    "key_l1_2": {
        "key_l2": "hello"
    },
    "key_l1_3": {
        "key_l2_2": {
            "key_l3": "hello"
        }
    }
}
```
For multi level json message, I want to `flatten` only just one level, like this:
```
{
    "key_l1": "value",
    "key_l1_2_key_l2": "hello",
    "key_l1_3_key_l2_2": {
         "key_l3": "hello"
    }
}
```
But I think it's more common to convert object to string.

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

_No response_

### Version

_No response_
