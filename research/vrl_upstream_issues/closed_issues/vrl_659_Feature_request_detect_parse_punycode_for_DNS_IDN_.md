# Issue #659: Feature request: detect, parse punycode for DNS IDN objects

- **URL:** https://github.com/vectordotdev/vrl/issues/659
- **Author:** @johnhtodd
- **Status:** CLOSED (completed)
- **Created:** 2024-01-26T08:41:48Z
- **Closed:** 2024-02-07T15:09:26Z
- **Labels:** vrl:stdlib

## Description

Any system that digests DNS data for more than a few hostnames will eventually get IDN names (https://unicode.org/faq/idn.html) in the data stream. This quickly presents problems for back-end data store and monitoring systems.

Systems may choose to keep IDN in their existing form, but having the ability to add fields which are encoded in punycode (https://en.wikipedia.org/wiki/Punycode) is desirable, as many DNS logging systems expect and use punycode to simplify management of handling IDN objects.

There are two three things which I think would be useful to have in Vector:
 - the ability to detect if a field contains characters which are present in IDN-formatted strings
 - the ability to convert IDN names into punycode from UTF-8
 - the ability to convert IDN names from punycode into UTF-8

There appear to be several existing Rust libraries which do this type of conversion. I don't know which have what desirable features or preferred licenses, so I won't make references here so as not to bias any search.

Notes: 
  - this is DNS-specific.  The conversion would have to be applied to each "zone cut" between periods, but portions of the name that do not have UTF-8 would not be translated.  So www.café.com would be www.xn--caf-dma.com as an example.
  -  lowercasing the name is automatically assumed.  So www.CAFé.com and www.cafÉ.com would also be www.xn--caf-dma.com
