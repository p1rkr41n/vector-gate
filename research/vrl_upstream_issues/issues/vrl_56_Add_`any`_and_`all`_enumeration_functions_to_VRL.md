# [#56] Add `any` and `all` enumeration functions to VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/56)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-06-08T07:31:27Z`
- **Updated At**: `2026-06-01T14:16:55Z`
- **Comments**: 3
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/56)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

Now that [iteration support has landed in VRL](https://vector.dev/highlights/2022-05-18-vrl-iteration-support/), we can look at introducing additional convenience functions.

Two of those functions that are often mentioned on Discord and GH issues are `any` and `all`.

For example, in vectordotdev/vector#9068, a request was made to check `ip_cidr_contains` against a list of functions.

This could be achieved using the following iteration logic:

```coffee
contains = false
for_each(["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]) -> |_index, ip| {
	if ip_cidr_contains(ip, .ip_src) ?? false {
		contains = true
	}
}
contains
```

But with `any`, this could be shortened to:

```coffee
any(["10.0.0.0/8", "172.16.0.0/12", "192.168.0.0/16"]) { |_index, ip|
	ip_cidr_contains(ip, .ip_src) ?? false
}
```

We'll also add `all`, which only returns `true` if all steps in the iterator return `true`.

