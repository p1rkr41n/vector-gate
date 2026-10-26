# [#854] Multiline expressions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/854)
- **Status**: `OPEN`
- **Author**: [@hamishforbes](https://github.com/hamishforbes)
- **Created At**: `2024-05-23T22:01:42Z`
- **Updated At**: `2024-05-24T14:12:45Z`
- **Comments**: 1
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/854)

---

## Description

I'm just getting starting with Vector and I'm struggling with just laying out complex if statements over multiple lines.

This is I guess part doc request, I haven't found anything in the docs that describes how to split expressions over multiple lines
and part feature request to improve the support here

As an example I have a vrl remap to drop noisy/useless log lines
one of the statements in that program is this, which works

```
if .kubernetes.pod_labels."common.k8s.elastic.co/type" == "elasticsearch" &&
  (contains(.message, "cname_in_publish_address") ||
  contains(.message, "Fielddata access on the ")) { abort }
```

but this syntax feels a bit awkward and ideally I'd like to do something like this

```
if .kubernetes.pod_labels."common.k8s.elastic.co/type" == "elasticsearch"
  && (
    contains(.message, "cname_in_publish_address")
    || contains(.message, "Fielddata access on the ")
  )
{ abort }
```

Which is invalid but I don't really understand why.
