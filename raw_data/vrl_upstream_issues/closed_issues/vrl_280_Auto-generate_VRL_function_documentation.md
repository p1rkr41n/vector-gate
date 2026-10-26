# Issue #280: Auto-generate VRL function documentation

- **URL:** https://github.com/vectordotdev/vrl/issues/280
- **Author:** @fuchsnj
- **Status:** CLOSED (completed)
- **Created:** 2023-06-28T15:02:56Z
- **Closed:** 2026-03-07T19:33:45Z
- **Labels:** None

## Description

## Problem
Before the VRL repo was split from Vector, VRL function documentation was manually added for each change in CUE docs. Now since the repo is split, there is currently no way to add / update documentation with each PR. Even before, it was easy for documentation to become out of date since it's manually updated and nothing is checking it for accuracy.

## Proposal
The source of documentation will live wherever VRL functions are defined. (The VRL repo for stdlib functions, or other repos for user added functions, such as Vector specific VRL functions). This will be auto-generated directly from the code (function name, parameters, examples, .etc) and supplemented by annotations were needed. This will be roughly similar to Vector's [config schema](https://github.com/vectordotdev/vector/blob/master/rfcs/2022-02-23-9481-config-schema.md)

The VRL repo will contain a tool that can generate a computer-readable intermediate format of the function documentation in JSON. This allows end-users of VRL to generate documentation from the intermediate format.

For example:
- Vector would generate the intermediate JSON format for the stdlib functions, as well as several Vector specific functions, and then convert that to CUE docs for the documentation [here](https://vector.dev/docs/reference/vrl/functions/)
- VRL itself may one day host it's own documentation for just the stdlib. The intermediate format gives flexibility to use whatever tool makes sense for the job, instead of having to copy what Vector is currently using.
- The VRL playground (or Observability Pipelines) could ingest this data as they wish to improve the related UI.
- Future users of VRL could integrate this data into their own documentation.

