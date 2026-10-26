# Issue #1497: FR: Allow http_request function to send request body

- **URL:** https://github.com/vectordotdev/vrl/issues/1497
- **Author:** @monwolf
- **Status:** CLOSED (completed)
- **Created:** 2025-09-01T13:20:55Z
- **Closed:** 2025-09-05T16:38:51Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

The http_request function in VRL currently allows making HTTP requests by specifying method, headers, and URL. However, it does not support sending a request body.

This limits its use mainly to GET or HEAD operations and makes it impossible to interact with endpoints that require a payload in POST, PUT, or PATCH requests.

Benefits:

Enables full interaction with REST APIs directly from VRL.
Reduces the need for external processors to enrich or validate data.
Increases VRL’s flexibility in enrichment and transformation scenarios.

Expected impact:
Backward compatible: existing usage remains unchanged if body is not provided.
Adds significant value without breaking existing functionality.

### Use Cases

My current use case is to send the logs to an external anonymizer 

### Attempted Solutions

I had to change the current service to accept values via query string

### Proposal

Proposal:
Introduce an optional body parameter to the http_request function that would accept:

A plain string (e.g., serialized JSON).

(Optionally) a map that can be automatically serialized depending on the Content-Type.

### References

https://github.com/vectordotdev/vrl/pull/1360

