# Issue #4482: Grok parser: provide an option to allow for removing empty matches

- **URL:** https://github.com/vectordotdev/vector/issues/4482
- **Author:** @itkovian
- **Status:** CLOSED (completed)
- **Created:** 2020-10-09T20:11:03Z
- **Closed:** 2020-12-21T21:27:20Z
- **Labels:** domain:parsing, domain:vrl

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
vector 0.11.0 (ga6248f5 x86_64-unknown-linux-gnu 2020-10-08)
```

### Use-cases

<!---
In order to properly evaluate a feature request, it is necessary to understand the use-cases for it.

Please describe below the _end goal_ you are trying to achieve that has led you to request this feature.

Please keep this section focused on the problem and not on the suggested solution. We'll get to that in a moment, below!
-->

When using the grok parser that has a `(%{A:a}|%{B:b})` somewhere in the parse tree, one of these items will end up being empty in the resulting parsed structure. This means that each grok result will have a set containing all matched and non-matched fields, which is not really usable, especially when the parser needs to produce distinct "objects" for each message type.


### Attempted Solutions

<!---
If you've already tried to solve the problem within Vector's existing features and found a limitation that prevented you from succeeding, please describe it below in as much detail as possible.

Ideally, this would include real configuration snippets that you tried and what results you got in each case.

Please remove any sensitive information such as passwords before sharing configuration snippets and command lines.
--->

I took a look at the `remove_fields` transform but alas, that only drops empty parents after removing the provided list of fields, which is not really what is needed: `If set to true, after removing fields, remove any parent objects that are now empty.`


### Proposal

Similar to the grok parser in logstash, having a `keep_empty_captures` option that defaults to `no`, would remove all the fields that are empty after matching the line. 

<!---
If you have an idea for a way to address the problem via a change to Vector features, please describe it below.

In this section, it's helpful to include specific examples of how what you are suggesting might look in configuration files, or on the command line, since that allows us to understand the full picture of what you are proposing.

If you're not sure of some details, don't worry! When we evaluate the feature request we may suggest modifications as necessary to work within the design constraints of Vector.
-->

### References

<!--
Are there any other GitHub issues, whether open or closed, that are related to the problem you've described above or to the suggested solution? If so, please create a list below that mentions each of them. For example:

- #7023

-->

- #4430 

