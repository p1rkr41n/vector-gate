# Issue #264: parse_key_value interprets the next key-value pair as the value of the current key

- **URL:** https://github.com/vectordotdev/vrl/issues/264
- **Author:** @aryanbaghi
- **Status:** CLOSED (completed)
- **Created:** 2023-06-04T15:36:21Z
- **Closed:** 2023-06-06T19:34:59Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

When using `parse_key_value` in the remap transformation for logs like this:

```
level=info msg="Removed endpoint" containerID= datapathPolicyRevision=2 desiredPolicyRevision=2 endpointID=2213 identity=21332 ipv4= ipv6= k8sPodName=/ subsys=endpoint
```

For null-valued keys, we get this output:
```
{
    ...
    'containerID': 'datapathPolicyRevision=2'
}
```

Even when we add whitespace, the "strict" issue is not resolved.

### Configuration

_No response_

### Version

0.30.0

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
