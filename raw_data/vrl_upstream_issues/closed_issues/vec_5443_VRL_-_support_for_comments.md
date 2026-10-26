# Issue #5443: VRL - support for comments

- **URL:** https://github.com/vectordotdev/vector/issues/5443
- **Author:** @spencergilbert
- **Status:** CLOSED (completed)
- **Created:** 2020-12-08T19:00:46Z
- **Closed:** 2021-01-12T15:29:35Z
- **Labels:** domain:vrl

## Description

<!--
Hi there,

Thank you for opening an issue. Please note that we try to keep the Vector issue tracker reserved for bug reports and feature requests. For general usage questions, please see: https://chat.vector.dev.
-->

### Current Vector Version

<!---
Run `vector --version` to show the version, and paste the result between the ``` marks below. This will record which version was current at the time of your feature request, to help manage the request backlog.

If you're not using the latest version, please check to see if something related to your request has already been implemented in a later version.
-->

```
vector 0.12.0 (gb1d0189 x86_64-unknown-linux-musl 2020-12-08)
```

### Use-cases

<!---
In order to properly evaluate a feature request, it is necessary to understand the use-cases for it.

Please describe below the _end goal_ you are trying to achieve that has led you to request this feature.

Please keep this section focused on the problem and not on the suggested solution. We'll get to that in a moment, below!
-->
Describing the functionality of remap configuration _next to_ the actions themselves, documentation of what the transformation is/should be doing

### Attempted Solutions

<!---
If you've already tried to solve the problem within Vector's existing features and found a limitation that prevented you from succeeding, please describe it below in as much detail as possible.

Ideally, this would include real configuration snippets that you tried and what results you got in each case.

Please remove any sensitive information such as passwords before sharing configuration snippets and command lines.
--->
Right now I've been doing this as `toml` comments above/below the remap _source_ key, which works but as the remap becomes longer or more complex it's more difficult to understand.

### Proposal

<!---
If you have an idea for a way to address the problem via a change to Vector features, please describe it below.

In this section, it's helpful to include specific examples of how what you are suggesting might look in configuration files, or on the command line, since that allows us to understand the full picture of what you are proposing.

If you're not sure of some details, don't worry! When we evaluate the feature request we may suggest modifications as necessary to work within the design constraints of Vector.
-->
Inclusion of comments for TRL using something like `//`, `#`, etc

### References

<!--
Are there any other GitHub issues, whether open or closed, that are related to the problem you've described above or to the suggested solution? If so, please create a list below that mentions each of them. For example:

- #7023

-->

