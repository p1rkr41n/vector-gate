# Issue #660: Feature request: CDB for enrichment table source

- **URL:** https://github.com/vectordotdev/vrl/issues/660
- **Author:** @johnhtodd
- **Status:** CLOSED (not_planned)
- **Created:** 2024-01-26T09:06:18Z
- **Closed:** 2024-01-29T14:58:10Z
- **Labels:** vrl:stdlib

## Description

We currently use DJB's Constant DataBase (CDB - https://en.wikipedia.org/wiki/Cdb_(software) )   as a source for matching lists in our DNS environment, in the "front-end" systems that see hundreds of thousands or millions of requests per second.  It's quite performant, especially coupled with caching by the local application that is performing the queries.

In the logging stream (DNSTAP) we would also like to use CDB, as this would require no conversion of some of our existing tooling, and would be well-suited for large data set matching and enrichment that would be specific to how we envision using Vector. 

Note: it is fairly trivial to turn CDB into CSV, which might match well with the existing Vector CSV enrichment system. That can mean one of two (or more) options: make the user turn CDB into CSV to avoid the development work, or create an adapter that treats CDB files as CSV and simply converts them at load time. (https://github.com/vectordotdev/vector/blob/13b914781b3c118cbf867609ebab5d5fc6a525dc/rfcs/2021-07-20-8288-csv-enrichment.md) 

I do have a question about CSV functionality, which is why I reference CDB: how are reloads managed? CDB files handle switchout for new data sets exceptionally well, and that is implicit in CDB's model. CSV files as enrichment sources in Vector are less clear - CSV is loaded into memory, but how is that updated without a full restart?

Meta-summary:

Basic desired functionality;
 - Lookup key in CDB, return multi-value results
 - Cache answers (including "no match") for N milliseconds or until CDB file changes (datestamp/size) as checked every N seconds, for performance

There seem to be Rust implementations of CDB, but again I'll not put any suggestions in here as my search-engine based answers in no way should resemble development ideas.  :-)

