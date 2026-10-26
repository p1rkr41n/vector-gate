# [#1313] Add option for VRL function parse_key_value to specify resulting key case

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1313)
- **Status**: `OPEN`
- **Author**: [@alexeynl](https://github.com/alexeynl)
- **Created At**: `2025-03-03T16:48:00Z`
- **Updated At**: `2026-06-16T13:09:36Z`
- **Comments**: 4
- **Labels**: `vrl:stdlib`, `stdlib:parse_key_value`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1313)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases


Lets we have the following strings:
```
key1=value1,key2=value2
Key1=value1,Key2=value2
```
In current implementation using 
```
result = parse_key_value(string)
```
i need check both
```
result.key1
result.Key1
```
for value.

 


### Attempted Solutions

_No response_

### Proposal

If i have keys in key value string contains in different cases i need option to specify case of resulting field names like this:
```
result = parse_key_value(string, key_case: "low")
```
result.key1 must return value1 for both string:
```
key1=value1,key2=value2
Key1=value1,Key2=value2
```
### References

_No response_

### Version

_No response_
