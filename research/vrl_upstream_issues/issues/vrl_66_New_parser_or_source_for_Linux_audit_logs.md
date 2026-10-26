# [#66] New parser or source for Linux audit logs

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/66)
- **Status**: `OPEN`
- **Author**: [@kierdavis](https://github.com/kierdavis)
- **Created At**: `2022-05-05T12:33:02Z`
- **Updated At**: `2026-06-01T14:16:46Z`
- **Comments**: 6
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/66)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Use Cases

The Linux kernel can provide a stream of audit logs, which allows system administrators to observe high-level security-related events without needing to trust every process to faithfully log what it is doing. This is accessible through a kernel API, but most Linux operating systems include a userspace service (auditd) to transfer these logs to a human-readable file on disk.

In an environment with hundreds of servers where system security is a major concern, I would like to build tooling to aggregate these audit logs at scale and deliver notifications when unusual activity is detected. Additionally, the audit log records when any operation is denied due to the active SELinux policy, so being able to aggregate these denials across many hosts would be useful when developing and tuning the SELinux policy.

### Attempted Solutions

Obviously you can ingest audit.log using the `file` source, but only as plain text. The data is structured and it would be useful to be able to access the individual fields in Vector for analysis/routing purposes.

At first glance it might look like you could parse it with `parse_key_value`, but it is subtly more complex. For example, given this log line:

```
type=USER_LOGOUT msg=audit(1651746068.966:32475): pid=122482 uid=0 auid=0 ses=146 subj=system_u:system_r:sshd_t:s0-s0:c0.c1023 msg='op=login id=0 exe="/usr/sbin/sshd" hostname=? addr=1.2.3.4 terminal=ssh res=success' UID="root" AUID="root" ID="root"
```

This looks like a really strange format, but makes slightly more sense when you realise that this part:

```
audit(1651746068.966:32475): pid=122482 uid=0 auid=0 ses=146 subj=system_u:system_r:sshd_t:s0-s0:c0.c1023 msg='op=login id=0 exe="/usr/sbin/sshd" hostname=? addr=1.2.3.4 terminal=ssh res=success'
```

is the raw text emitted by the kernel, which auditd substitutes (unquoted) into a template like this:

```
type=USER_LOGOUT msg=<raw line> UID="root" AUID="root" ID="root"
```

If you try to pass this line to `parse_key_value`, it sees two pairs with the same key: `msg=audit(1651746068.966:32475):` and `msg='op=login`. Only the latter is kept; the former (which contains the timestamp!) is lost. This could be worked around by splitting the line somewhere in between e.g. immediately after the `msg=audit(...):` token.

Also, we end up with `msg='op=login` and `res=success'` but `op=login` and `res=success` would be more useful. This is due to `parse_key_value` only recognising double-quoted values, not single-quoted ones. Again, this can be worked around with string manipulation functions.

Currently we're using individual regexes to extract just the fields that we're interested in. It would be nice to have a general solution for parsing these logs.

### Proposal

#### A hacky solution

Extend `parse_key_value` to understand single-quoted values as well as double-quoted ones.
Together with some string splitting, regexing, and timestamp parsing, these log lines can be fully parsed.
A "recipe" for this could be included in the examples section of the docs.

#### A good solution

The above solution requires a lot of VRL code, which everyone who wants to parse this log would have to duplicate. There is already precedent for having many specialised VRL functions for parsing different formats, so we could introduce a new one for parsing the auditd log format.

Example VRL (same input string as discussed above):

```
parse_auditd(s'type=USER_LOGOUT msg=audit(1651746068.966:32475): pid=122482 uid=0 auid=0 ses=146 subj=system_u:system_r:sshd_t:s0-s0:c0.c1023 msg=\'op=login id=0 exe="/usr/sbin/sshd" hostname=? addr=1.2.3.4 terminal=ssh res=success\' UID="root" AUID="root" ID="root"')
```

Return value:

```json
{
  "type": "USER_LOGOUT",
  "timestamp": "2022-05-05T10:21:08.966Z",
  "counter": 32475,
  "pid": 122482,
  "uid": 0,
  "auid": 0,
  "ses": 146,
  "subj": "system_u:system_r:sshd_t:s0-s0:c0.c1023",
  "msg": {
    "op": "login",
    "id": 0,
    "exe": "/usr/bin/sshd",
    "hostname": "?",
    "addr": "1.2.3.4",
    "terminal": "ssh",
    "res": "success"
  },
  "UID": "root",
  "AUID": "root",
  "ID": "root"
}
```

Alternatively the contents of the `msg` object could be flattened into the top-level object. I don't have a preference on this.

#### A better solution

The above solution will break if auditd ever changes its logging format. Since the file it writes to is intended to be human-readable, this is entirely possible.

A more robust (but more complex) solution would be to implement a new source which skips auditd's serialisation and uses the kernel API (via `libaudit.so`) instead.

### References

This may be a duplicate of an existing issue - there's some 200 issues mentioning the word "audit" and I haven't checked all of them.

### Version

vector 0.21.1 (x86_64-unknown-linux-gnu 18787c0 2022-04-22)
