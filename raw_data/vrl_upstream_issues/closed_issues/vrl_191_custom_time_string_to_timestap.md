# Issue #191: custom time string to timestap 

- **URL:** https://github.com/vectordotdev/vrl/issues/191
- **Author:** @MzCqueF56s6Z
- **Status:** CLOSED (completed)
- **Created:** 2023-04-13T06:06:03Z
- **Closed:** 2023-04-13T15:19:38Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

this string :   2023-04-10 09:40:20,042 ,can't use to_timestamp() .
may be we need  
```to_timestamp("2023-04-10 09:40:20,042","%F %T,%.3f")```    
just like  this:
```NaiveDate::parse_from_str("2023-04-10 09:40:20,042","%F %T,%.3f").unwrap();```

### Attempted Solutions

_No response_

### Proposal

_No response_

### References

_No response_

### Version

vector 0.29.0
