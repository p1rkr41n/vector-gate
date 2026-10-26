# [#131] VRL: syslog priority parsing 

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/131)
- **Status**: `OPEN`
- **Author**: [@rwaweber](https://github.com/rwaweber)
- **Created At**: `2021-03-25T21:27:18Z`
- **Updated At**: `2023-04-04T14:56:12Z`
- **Comments**: 2
- **Labels**: `type:enhancement`, `vrl:stdlib`, `good first issue`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/131)

---

## Description

### Current Vector Version
0.12.1

### Use-cases
"The Priority value is calculated by first multiplying the Facility number by 8 and then adding the numerical value of the Severity." 
~ [cite](https://tools.ietf.org/html/rfc5424#page-11) from RFC5424

e.g.:
```
Priority = Facility * 8 + Severity 

Facility = Priority % 8
Severity = Priority // 8
```

Sometimes, when dealing with non-rfc-compliant syslog variations, only parts of the RFC are followed. In those cases, its not uncommon for the syslog priority to be one of the only consistent distinguishing features of somelogs.

Being able to extract both the facility and severity code from those messages would be pretty handy, and from a cursory overview, looks like it would fit in pretty nicely as a VRL function.

### Attempted Solutions
None as of yet.

### Proposal

Add `to_syslog_facility_from_priority` and `to_syslog_severity_from_priority` functions to VRL for making use of Syslog Priority fields.

Or just one function with three return values(Facility, Severity, Error), what do you all think?

One more question, I noticed that we use the `syslog_loose` create which has a [`decompose_pri`](https://docs.rs/syslog_loose/0.10.0/src/syslog_loose/pri.rs.html#154-162) function that pretty much takes care of what I'm talking about.
Would you all have a preference for using _that_ over just implementing it in this plugin? I don't imagine it'd change how much code ends up there in either case, but I figured it's probably worth asking.

### References

Related in spirit: https://github.com/timberio/vector/issues/5769
