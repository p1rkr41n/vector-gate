# [#80] Add function for repeating a string to VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/80)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2022-02-01T18:28:07Z`
- **Updated At**: `2026-06-01T14:16:33Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/80)

---

## Description

<!--
Hi there,

Thank you for opening an issue. Please note that we try to keep the Vector issue tracker reserved for bug reports and feature requests. For general usage questions, please see: https://chat.vector.dev.
-->

<!--- Please keep this note for the community --->

### Community Note

* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment

<!--- Thank you for keeping this note for the community --->

### Current Vector Version

<!---
Run `vector --version` to show the version, and paste the result between the ``` marks below. This will record which version was current at the time of your feature request, to help manage the request backlog.

If you're not using the latest version, please check to see if something related to your request has already been implemented in a later version.
-->

```
vector 0.19.1 (x86_64-apple-darwin 3cf70cf 2022-01-25)
```

### Use-cases

Users may want to repeat a string a number of times.

### Attempted Solutions

We currently do support this in an undocumented fashion via the multiplication operator, for example: `"some string" * 5`

### Proposal

We add a specialized function for repeating a string that can be fallible that can be called like `repeat("some string", 5)`.

### References

<!--
Are there any other GitHub issues, whether open or closed, that are related to the problem you've described above or to the suggested solution? If so, please create a list below that mentions each of them. For example:

- vectordotdev/vector#7023

-->

