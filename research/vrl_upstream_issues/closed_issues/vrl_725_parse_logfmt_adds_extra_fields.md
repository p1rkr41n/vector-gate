# Issue #725: parse_logfmt adds extra fields

- **URL:** https://github.com/vectordotdev/vrl/issues/725
- **Author:** @ofirmad
- **Status:** CLOSED (completed)
- **Created:** 2024-01-08T14:04:35Z
- **Closed:** 2024-03-13T14:52:51Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I use parse_logfmt and I get field which I didn't expect to get.

in the following link you can see **"\\t\\t\"": true** in the output. This field should be part of errorVerbose value, it should be standalone field.
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoibG9nLCBlcnIgID0gIHBhcnNlX2xvZ2ZtdCgubWVzc2FnZSlcbi4gPSBtZXJnZSguLCBsb2cpIiwiZXZlbnQiOnsibWVzc2FnZSI6ImxldmVsPWVycm9yIGVycm9yVmVyYm9zZT1cImNhbm5vdCBcXHRcXHRcIiJ9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

but if I take one '\' off I get a good output, without extra fields
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoibG9nLCBlcnIgID0gIHBhcnNlX2xvZ2ZtdCgubWVzc2FnZSlcbi4gPSBtZXJnZSguLCBsb2cpIiwiZXZlbnQiOnsibWVzc2FnZSI6ImxldmVsPWVycm9yIGVycm9yVmVyYm9zZT1cImNhbm5vdCBcdFxcdFwiIn0sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9

I would expect to get errorVerbose value as one line value, without being split, for example:
{
	"errorVerbose": "cannot \\t\\t",
	"level": "error",
	"message": "level=error errorVerbose=\"cannot \\t\\t\""
}

I can see the extra fields is added when there is \\x\\y pattern inside the value in the input (x is a single character, y can be any string).

Thanks.

### Configuration

_No response_

### Version

0.24.1

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
