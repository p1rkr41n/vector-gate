# [#348] VRL is not a "safe" language in some environments

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/348)
- **Status**: `OPEN`
- **Author**: [@collimarco](https://github.com/collimarco)
- **Created At**: `2023-07-25T18:58:34Z`
- **Updated At**: `2026-06-01T14:18:03Z`
- **Comments**: 6
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/348)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

I have a service that receives some logs and I was thinking about using VRL for allowing customers of the service to apply transformations to the logs (which is the goal of this project).

In the official documentation I read sentences like this:

> VRL is a safe language in several senses: VRL scripts have access only to the event data that they handle and not, for example, to the Internet or the host;

Then I found functions like `get_env_var` which is definitely not safe in a shared environment (e.g. a multi-tenant SaaS). That function **allows sensitive information of the host to leak in the logs**. A similar issue is related to `get_hostname`. I think that these functions are not "safe" because they allow access to some inputs (e.g. ENV, hostname) that are not present in the logs, escaping the isolation that someone expects when running a VRL on the logs. 

### Configuration

_No response_

### Version

latest

### Debug Output

_No response_

### Example Data

_No response_

### Additional Context

_No response_

### References

_No response_
