# Issue #720: Add "dns_lookup" function

- **URL:** https://github.com/vectordotdev/vrl/issues/720
- **Author:** @johnhtodd
- **Status:** CLOSED (completed)
- **Created:** 2024-03-03T01:54:26Z
- **Closed:** 2024-05-06T18:25:14Z
- **Labels:** None

## Description

We have a need to perform lookups on DNS results delivered to us via the DNSTAP source, to determine (as an example) if an error is transient, or is related to a specific geography of resolvers that may be malfunctioning. Also, some DNS requests may yield lookup data in some cases, where a TXT or other result can be used to enrich the logging message as it moves through Vector, or where NS records may be used to enrich data such as "What authoritative nameserver cluster provided these answers?"

We would therefore like to request this as a VRL feature to be added to Vector that allows DNS requests to be emitted from Vector, and the result of those queries to be handed back in some easily parseable way.   The good news is that there already exists a DNSTAP structure, and so this would require grafting an existing Rust-based resolver library to produce results that could be fed to the DNSTAP parser as replies.

There are caveats here, and that is understood. These may be slow processes - the DNS is not easily predicted for response times. Local caches should be used, possibly on the same server as Vector is operating, in order to accelerate results. Timeouts and retries for failures should probably be kept low as a best-practice - "fail fast."  Simply because this may be slow is not sufficient to not perform the lookups - we will probably execute these on a sampled set of events in order to tune an adequate response rate to the stream of total inbound events we need to parse.

This would specifically not allow queries for QTYPEs of AXFR, IXFR, or ANY as they are too complex to easily render and are difficult to imagine in a Vector use case.

Ideally these fields would be used:

 - qname (mandatory)
 - QTYPE (mandatory)
 - namesever destination (optional - if not specified, system resolver will be used)
 - options (optional)
 - class (optional, default IN)

The reply from the resolver code would be handed back as a DNSTAP message structure.

Example:

`.myDnsResult = dns_lookup!("www.example.com", "9.9.9.9", "A", ["timeout=1", "tries=1", "nodnssec", "nsid"])
`

Errors in the DNS lookup should not produce errors within Vector, unless they are invalid command options which cannot be parsed. NXDOMAIN, SERVFAIl, etc. are all legitimate responses from the resolver stack, and should be represented in the DNSTAP message and not raise an error in Vector.  Only if the syntax of the command is incorrect should the lookup fail with an error outcome that is fallible, or if there is a timeout in the response (should this be a fixed number like 5 seconds?) or if there is some problem executing the command like no sockets available or no route to IP address for the recursive resolver.

This option list cribbed from recent Debian "dig" options that seem relevant and which are not redundant:

Options:
```
   [no]aaflag         (Set AA flag in query ([no]aaflag))
   [no]adflag         (Set AD flag in query (default on))
   [no]badcookie      (Retry BADCOOKIE responses)
   bufsize[=###]      (Set EDNS0 Max UDP packet size)
   [no]cdflag         (Set checking disabled flag in query)
   [no]cookie         (Add a COOKIE option to the request)
   [no]dns64prefix    (Get the DNS64 prefixes from ipv4only.arpa)
   [no]dnssec         (Request DNSSEC records)
   [no]edns[=###]     (Set EDNS version) [0]
   ednsflags=###      (Set EDNS flag bits)
   [no]ednsnegotiation (Set EDNS version negotiation)
   ednsopt=###[:value] (Send specified EDNS option)
   noednsopt          (Clear list of ednsopt options)
   [no]expire         (Request time to expire)
   [no]fail           (Don't try next server on SERVFAIL)
   [no]header-only    (Send query without a question section)
   [no]ignore         (Don't revert to TCP for TC responses.)
   ndots=###          (Set search NDOTS value)
   [no]nsid           (Request Name Server ID)
   [no]nssearch       (Search all authoritative nameservers)
   [no]opcode=###     (Set the opcode of the request)
   padding=###        (Set padding block size [0])
   qid=###            (Specify the query ID to use when sending queries)
   [no]raflag         (Set RA flag in query ([no]raflag))
   [no]recurse        (Recursive mode ([no]rdflag))
   retry=###          (Set number of UDP retries) [2]
   subnet=addr        (Set edns-client-subnet option)
   [no]tcflag         (Set TC flag in query)
   [no]tcp            (TCP mode)
   timeout=###        (Set query timeout) [5]
   tries=###          (Set number of UDP attempts) [3]
   [no]zflag          (Set Z flag in query)


```
