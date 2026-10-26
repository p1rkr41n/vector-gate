# [#1576] Add ed25519 signing

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1576)
- **Status**: `OPEN`
- **Author**: [@Reasonable-Solutions](https://github.com/Reasonable-Solutions)
- **Created At**: `2025-12-03T18:23:29Z`
- **Updated At**: `2026-06-01T14:19:43Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1576)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Use Cases

use case: 
When ingesting or transforming security related events it is often good and cool to have 
chain of custody and tamper evidence.  This is also neat to have when discussing compliance and audit trails. 
This can be achieved by signing the data at each step or service 

 
 


### Attempted Solutions

_No response_

### Proposal

I'm thinking something like 
```vrl
.signature = ed25519_sign!(.data, key: "/path/to/private.key") 
```
and with the implementation being basically wrapping dalek primitives  
```rust  
fn ed25519_sign(data: Value, key_path) -> Result<Value> {
.. steps  
  Ok(base64::encode(signature.to_bytes()).into())
}
```

### References

_No response_
