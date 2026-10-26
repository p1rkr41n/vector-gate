# [#1297] Introduce `break` for aborting iterations

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1297)
- **Status**: `OPEN`
- **Author**: [@dr4gon123](https://github.com/dr4gon123)
- **Created At**: `2025-02-25T04:24:52Z`
- **Updated At**: `2026-06-01T14:19:16Z`
- **Comments**: 1
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1297)

---

## Description

based on this [discussion](https://github.com/vectordotdev/vrl/discussions/1293#discussioncomment-12174840) 

a nice feature would be to have a `break` instruction to finish an ongoing iteration, like when you iterate on a `for_each` instruction like in

```
      # Define a map of IP ranges and their classifications
      range_map = {
          "10.0.0.0/8": "private",
          "172.16.0.0/12": "private",
          "192.168.0.0/16": "private",
          "127.0.0.0/8": "loopback",
          "169.254.0.0/16": "link_local",
          "224.0.0.0/4": "multicast",
          "100.64.0.0/10": "carrier_nat",
          "192.0.0.0/24": "documentation",
          "192.0.2.0/24": "documentation",
          "198.51.100.0/24": "documentation",
          "203.0.113.0/24": "documentation",
          "240.0.0.0/4": "reserved",
          
          # IPv6 Ranges
          "::1/128": "loopback",
          "fc00::/7": "private",  # Unique Local Addresses (ULA)
          "fe80::/10": "link_local",
          "ff00::/8": "multicast",
          "100::/64": "discard",  # RFC 6666
          "2001:db8::/32": "documentation",  # RFC 3849
          "2002::/16": "6to4_tunnel",
          "::ffff:0:0/96": "ipv4_mapped",
          "::/128": "unspecified",
          "::ffff:0:0:0/96": "ipv4_translated",
          "2001::/23": "reserved",  # IANA reserved block
          "4000::/2": "reserved"   # Reserved for future use
      }
      
      # Default to "public"
      .source.ip_type = "public"
      
      # Check which range the IP belongs to
      for_each(range_map) -> |cidr, ip_type| {
          if ip_cidr_contains!(cidr, to_string!(.source.ip)) {
              .source.ip_type = ip_type
          }
      }
```

it would be more efficient for sure if there would be a way to break the `for_each` iteration
```
      for_each(range_map) -> |cidr, ip_type| {
          if ip_cidr_contains!(cidr, to_string!(.source.ip)) {
              .source.ip_type = ip_type
              break
          }
      }
```

but `break` is not supported and reserved for future use
```
error[E205]: reserved keyword
   ┌─ :46:9
   │
46 │         break
   │         ^^^^^
   │         │
   │         this identifier name is reserved for future use in the language
   │         use a different name instead
   │
   = see language documentation at https://vrl.dev
   = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```


