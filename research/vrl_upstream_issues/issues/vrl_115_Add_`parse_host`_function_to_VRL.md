# [#115] Add `parse_host` function to VRL

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/115)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2021-05-12T13:18:02Z`
- **Updated At**: `2026-06-01T14:16:24Z`
- **Comments**: 2
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/115)

---

## Description

We had a [question in Discord](https://discord.com/channels/742820443487993987/764187584452493323/841976030520672276) how to get the [TLD](https://en.wikipedia.org/wiki/Top-level_domain) of a domain name:

> having strings like "qwe.domain.tld" and "qwe.asd.anotherdomain.tld" how can I receive last two items as strings? "domain.tld", "anotherdomain.tld"?

They decided on a solution like the following:

```swift
hostParts = split("qwe.asd.anotherdomain.tld", ".")
hostParts[-2] + "." + hostParts[-1] // "anotherdomain.tld"
``` 

The problem with this is that not all TLDs are a single word. E.g. `co.uk` is a well-known one, but there are _many_ others that are comprised of multiple names separated by a dot.

As a language that focusses on correctness and the principle of least surprise at runtime, and given that manipulating/checking domains is a common task in the observability space we're operating in, I think we can do better here.

---

I propose we add a new `parse_host` function to wrap the [`tldextract` crate](https://docs.rs/tldextract/0.5.1/tldextract/) that works like this:

```swift
hostParts = parse_host!("qwe.asd.anotherdomain.tld")
hostParts // { "domain": "anotherdomain", "subdomain": "qwe.asd", "suffix": "tld" }
```

The `tldextract` library has a local cache of TLDs to know what's part of the TLD and what's part of the domain. It also has an option to update this list at runtime, but I suggest we disable that, opting instead to update the crate occasionally when new TLDs need to be added to the cache.

Alternatively, we could update `parse_url` to add this information, but the problem there is that this function only works with a valid URL, which _requires_ a scheme to be present (e.g. `mydomain.co.uk` would be rejected, but `https://mydomain.co.uk` works), which seems impractical for this particular use-case.



