# [#502] Parsing auditd logs has issues due to a 0x1D character

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/502)
- **Status**: `OPEN`
- **Author**: [@alex-rowe](https://github.com/alex-rowe)
- **Created At**: `2023-10-04T01:04:32Z`
- **Updated At**: `2023-10-10T22:06:41Z`
- **Comments**: 2
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/502)

---

## Description

### Discussed in https://github.com/vectordotdev/vector/discussions/18712

<div type='discussions-op-text'>

<sup>Originally posted by **alex-rowe** September 29, 2023</sup>
When using `auditd` set to `log_format = ENRICHED` there is a "group separator" character between the existing fields and unenriched fields.

This causes Vector to not split on this field when using `parse_key_value`.

When attempting to use `strip_ansi_escape_codes`, this only removes the value, but we need to split on it.

When attempting to use `replace`, we get errors for `unexpected error: invalid escape character: \u`

An example log line would be:

```
type=SYSCALL msg=audit(1695946364.453:9863): arch=c000003e syscall=257 success=yes exit=8 a0=ffffff9c a1=7f8f9b31cd80 a2=80002 a3=0 items=1 ppid=8221 pid=9287 auid=4294967295 uid=0 gid=1002 euid=0 suid=0 fsuid=0 egid=1002 sgid=1002 fsgid=1002 tty=pts0 ses=4294967295 comm="sudo" exe="/usr/bin/sudo" key="logins"ARCH=x86_64 SYSCALL=openat AUID="unset" UID="root" GID="ssm-user" EUID="root" SUID="root" FSUID="root" EGID="ssm-user" SGID="ssm-user" FSGID="ssm-user"
```

And `key="logins"ARCH=x86_64` are shown as joined when viewing using `cat` or `tail` etc.

When using the transform `.message = parse_key_value!(string!(.message))` we get the following:

```
"key": "(null)\u001dARCH=x86_64",
```

Is there a recommended way we can replace `\u001d` with a whitespace before we send it to `parse_key_value` so that it properly gets picked up a two fields, not one?

I see this related issue from VRL https://github.com/vectordotdev/vrl/issues/148, can we get unicode escapes (https://doc.rust-lang.org/reference/tokens.html#unicode-escapes) added as options?

A separate question may be the possibility of a `parse_auditd` function.

Extra information here:
* https://github.com/linux-audit/audit-userspace/issues/140
* https://github.com/linux-audit/audit-documentation/wiki/SPEC-Audit-Event-Enrichment</div>
