# Issue #651: Feature request: public suffix (TLD and ETLD+1) parsing

- **URL:** https://github.com/vectordotdev/vrl/issues/651
- **Author:** @johnhtodd
- **Status:** CLOSED (completed)
- **Created:** 2024-01-23T08:52:46Z
- **Closed:** 2024-02-06T15:55:31Z
- **Labels:** vrl:stdlib, good first issue

## Description


We're using DNSTAP for ingestion of DNS data. One of the data fields that we're interested in storing separately in our archive is the TLD and ETLD+1 data, which means the top level domain (".com", ".ch", ".xyz") which is trivially easy, but also the portion of the domain which is the part that is handled by a registrar.  For .com, as an example, it is the name immediately to the left of ".com" - so "example.com" is ETLD+1 for the .com zone.  For other regions of the DNS, this break point is non-obvious, and the Mozilla Public Suffix Iist (PSL) is the well-known authority on defining where those domain breaks occur so that the correct number of zone cuts can be made to capture the ETLD+1.  I imagine that many logfiles have domain-based data in them that would be interesting to parse in this manner - not just DNSTAP-oriented data.

Doing this computation at the edge of our telemetry pipeline makes the most sense for us.  Vector seems like a good place to do it, but there is currently no function that does this. 

There is a Rust library for this functionality (https://github.com/1Password/passkey-rs/tree/main/public-suffix) but what the command/function would look like from within VRL is not immediately obvious to me so I won't make suggestions as to how it could look in any detail. The short form: It would be useful to have a function that would result with the TLD and ETLD+1 for a given Fully-Qualified Domain Name provided as input.  Or even a ETLD+N where "N" is define-able.

