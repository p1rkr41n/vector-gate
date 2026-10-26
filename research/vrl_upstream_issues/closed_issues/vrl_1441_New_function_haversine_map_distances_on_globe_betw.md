# Issue #1441: New function: haversine (map distances on globe between latitude/longitude pairs)

- **URL:** https://github.com/vectordotdev/vrl/issues/1441
- **Author:** @johnhtodd
- **Status:** CLOSED (completed)
- **Created:** 2025-07-01T18:39:25Z
- **Closed:** 2025-07-09T15:41:44Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

We enrich data with MMDB data sets, giving us lat/lon for event data. We plot events on a globe/map with rough location of client and rough location of endpoint (could be POP, could be a target host, could be a target nameserver looked up in an enrichment CSV.)  Events will have higher or lower "value" based on distance, or will be treated differently in visibility tooling based on distance.  In order to calculate this, we need a Haversine function to compute distance between two lat/lon pairs and insert that into each event at the edge of the telemetry system instead of doing post-processing.

### Attempted Solutions

External computation is possible, but requires looping events through some generic code, so that is basically a non-starter for us.

### Proposal

I propose a function called "haversine" that takes two lat/lon points, and a measurement system (miles, kilometers) and emits a distance and a bearing on the earth.

```
haversine(measurement:<miles|kilometers>, lat1:<latitude1>, lon1:<longitude1>, lat2:<latitude2>, lon2:<longitude2>)
```
This results in an object containing:
distance (numeric distance between lat1/lon1 and lat2/lon2 within 7 decimals of exactness.)
bearing (degrees of bearing between point1 and point2 with three decimal degrees of exactness)


latitudes and longitudes are real numbers which will be used to within 7 decimal places of exactness.

This might require a new function class called "Map Functions" in the documentation (https://vector.dev/docs/reference/vrl/functions/)

### References

_No response_

### Version

vector 0.48.0 (x86_64-unknown-linux-gnu)
