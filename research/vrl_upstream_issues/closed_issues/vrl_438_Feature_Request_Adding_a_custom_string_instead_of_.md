# Issue #438: [Feature Request] Adding a custom string instead of ellipsis on vector truncate

- **URL:** https://github.com/vectordotdev/vrl/issues/438
- **Author:** @Nirzak
- **Status:** CLOSED (completed)
- **Created:** 2023-09-03T04:58:06Z
- **Closed:** 2023-09-25T22:16:33Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

We want to make alerting for the events that have been truncated but an ellipsis is usually a more generic string to identify and any messages can have ellipsis on a log ingestion program if it's out of the viewing area of events. So if vector provides a feature so that we can add a custom string at the end of the truncated message. then we can set alerting based on that string. Making it through the truncate function would make it easier for us.

### Attempted Solutions

No

### Proposal

We can implement a function to add that custom string via vector truncate vrl function. just like the following

truncate("A long sentence.", limit: 11, custom_message: [event_truncated])

### References

_No response_

### Version

vector 0.30.0
