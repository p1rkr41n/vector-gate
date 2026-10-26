# Issue #5369: New `parse_apache_log` Remap function

- **URL:** https://github.com/vectordotdev/vector/issues/5369
- **Author:** @binarylogic
- **Status:** CLOSED (completed)
- **Created:** 2020-12-03T19:31:54Z
- **Closed:** 2021-03-04T23:14:42Z
- **Labels:** domain:vrl

## Description

Note, this overlaps with #5370. We should adjust that function to support the following formats (if it makes sense):

- [ ] Parses the Apache common format as described in the [flog project](https://github.com/mingrammer/flog#supported-formats)
- [ ] Parses the Apache combined format as described in the [flog project](https://github.com/mingrammer/flog#supported-formats)
- [ ] Parses the Apache error format as described in the [flog project](https://github.com/mingrammer/flog#supported-formats)

I'm open to splitting these out but wanted to go for the easiest / simplest UX since users ultimately just want to parse Apache logs.
