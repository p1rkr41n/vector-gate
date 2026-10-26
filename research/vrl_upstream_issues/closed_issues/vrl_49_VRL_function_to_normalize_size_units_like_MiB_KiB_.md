# Issue #49: VRL function to normalize size units like MiB, KiB, etc. to bytes

- **URL:** https://github.com/vectordotdev/vrl/issues/49
- **Author:** @jblang
- **Status:** CLOSED (completed)
- **Created:** 2022-06-28T19:19:40Z
- **Closed:** 2025-01-06T18:09:01Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

I frequently come across log messages containing sizes using human-readable units such as MB, KB, GB, or MiB, KiB, GiB. Normalizing these to bytes is a prerequisite for comparison and statistical analysis.

### Attempted Solutions

I can do this using an if statement but it adds a lot of repetitive code to every transformation where I need it.

### Proposal

Add a `normalize_bytes` function to VRL that will take a string specifying a size in human readable capacity units and return an integer number of bytes.  The function should:

- Accept a floating point or integer number for the numeric portion
- Accept and convert all of the common abbreviations for a particular capacity unit:
  - K, KB, KiB - kilobytes
  - M, MB, MiB - megabytes
  - G, GB, GiB - gigabytes
  - T, TB, TiB - terabytes
  - And so on...
- Round any fractional bytes obtained from the conversion up to the nearest integer 
- Assume binary units by default (multiples of 1024 instead of 1000)
- Have an optional parameter (`binary`) that when set to false uses multiples of 1000 instead of 1024
- Accept optional whitespace between the number and the unit
- Treat the units case-insensitively

### References

_No response_

### Version

0.22.2
