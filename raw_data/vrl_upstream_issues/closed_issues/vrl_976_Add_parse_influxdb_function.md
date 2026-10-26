# Issue #976: Add `parse_influxdb` function 

- **URL:** https://github.com/vectordotdev/vrl/issues/976
- **Author:** @jorgehermo9
- **Status:** CLOSED (completed)
- **Created:** 2024-08-05T11:25:04Z
- **Closed:** 2024-08-22T22:27:30Z
- **Labels:** vrl:stdlib

## Description

With the merge of https://github.com/vectordotdev/vector/pull/19637, we thought of using that decoder instead of a custom lua one (which takes a lot of cpu), but it seems that we have malformed line protocol messages and using the `decoding.codec=influxdb` option in sources does allow to route the malformed messages somewhere else, as the data is being dropped.

The alternative we see is to use a remap transform with a `parse_influxdb` function and `drop_on_abort=true`, so we can route the malformed data (`<component_id>.dropped`) to our custom lua decoder which is less strict.

In order to handle this failing line protocol messages, we think that a `parse_influxdb` vrl function is needed. The implementation should be very similar to https://github.com/vectordotdev/vector/blob/210ff0925d391213556f07bf6ce621967f0368ca/lib/codecs/src/decoding/format/influxdb.rs#L97 

Doubt: The source decoder option is `decoding.codec=influxdb` and not `decoding.codec=line_protocol`, shoud we call this function `parse_influxdb` in order to be consistent with the vector option? or should we change the vector config spec to use `decoding.codec=line_protocol`?
