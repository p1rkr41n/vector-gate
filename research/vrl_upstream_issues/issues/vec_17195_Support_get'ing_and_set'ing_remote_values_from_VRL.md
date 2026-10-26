# [#17195] Support get'ing and set'ing remote values from VRL

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/17195)
- **Status**: `OPEN`
- **Author**: [@MadsRC](https://github.com/MadsRC)
- **Created At**: `2023-04-21T19:25:10Z`
- **Updated At**: `2026-05-29T23:44:34Z`
- **Comments**: 11
- **Labels**: `domain:vrl`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/17195)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

### Log Enrichment

Vector source produces a log:

```json
{
"userID": "1234",
"message": "authentication successful"
}
```

A VRL remap transform queries enriches the log, using the `userID`, with data from an external system:

```json
{
"userID": "1234",
"username": "MadsRC",
"message": "authentication successful"
}
```

### Calculating user logins

Vector source produces a log:

```json
{
"userID": "1234",
"message": "authentication successful"
}
```

Vector VRL remap transform increments counter in external system using `userID` as the key and gets the new total. An `if` statement is used to check the new total (which would be total logins over a period of time) against a threshold, and determines if it should produce a new message to a destination (using the routing functionality of Vector) to notify that something bad is happening.

### Attempted Solutions

Data Enrichment can currently be done by hard-coding the enrichment data into VRL. While this is arguably faster than making several network calls to get the data, it is not very scaleable or dynamic.

### Proposal

I would like to see VRL, and by extension Vector, support looking up values, and potentially setting values, in a remote system, such as Redis, Memcached or maybe a Relational Database of sorts.

On top of allowing for data enrichment, this would also allow one to use VRL/Vector as a proper detection engine. While one can already use Vector/VRL for simple detections, having the ability to reference a remote state of sorts would allow for some cool event correlation use-cases.

It is pretty common to have some sort of pipeline in front of a large, expensive enterprise SIEM system like Elasticsearch or Splunk. If one used Vector in this pipeline, and Vector supported get'ing and set'ing values in remote systems, one could offload some of the costs of these enterprise systems by doing real-time detections while one is processing the data anyways.

I am imagining a VRL syntax like this:

```toml
[transforms.increment]
type = "remap"
inputs = ["logs"]
source = '''
  .username = getLookup(.userID)
  .timestamp = now()
'''
```

or

```toml
[transforms.increment]
type = "remap"
inputs = ["logs"]
source = '''
  .username = setLookup(.userID, .username)
  .timestamp = now()
'''
```

and then setting connection info for the `getLookup` and `setLookup` function in the global settings.

Alternatively, supporting specific clients could also be in scope, so that one could use some of the more specialised functions of the lookup store, such as Redis's `INCR` function.

An example of where Redis's `INCR` function would be helpful is in the use-case of tracking amount of failed logins:

```toml
[transforms.increment]
type = "remap"
inputs = ["logs"]
source = '''
  if .eventType == "authentication" && .outcome == "failure" {
    .failCount = incrLookup(.src, 1)
  }
'''

[transforms.route]
type = "route"
inputs = ["increment"]
[transforms.route.route]
type = "vrl"
source = ".failCount > 10"
```

The above example would use the `incrLookup` function to increment a counter in Redis by 1, where the key is the value of the `src` field. The function would then return the new number (or alternatively, one could call getLookup or similar on the value) which is stored in `failCount`. The value of `failCount` is then used in a route transform to determine if it should forward the event somewhere.

### References

_No response_

### Version

_No response_
