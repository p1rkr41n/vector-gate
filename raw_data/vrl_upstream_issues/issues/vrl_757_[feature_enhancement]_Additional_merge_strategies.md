# [#757] [feature enhancement] Additional merge strategies

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/757)
- **Status**: `OPEN`
- **Author**: [@prein](https://github.com/prein)
- **Created At**: `2024-03-20T18:19:15Z`
- **Updated At**: `2024-03-21T12:52:17Z`
- **Comments**: 0
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/757)

---

## Description

It would be great to be able to control merge function behavior when there are keys with the same name in "to" and "from" objects.
Current behavior for simple values is to use the value from object that enjoys higher precedence.
What I think could be sometimes helpful to be able to do instead:
* rename the key
* merge / concatenate the values from both keys
* store the conflicting keys in some other object

Example:

event:
```
{
  "json": {
    "msg": "bar"
  },
  "msg": "foo"
}
```
program:
```
. = merge!(del(.json), .)
```
output:
```
{
    "msg": "foo"
}
```

changing the precedence
program:
```
. = merge!(.,del(.json))
```
output:
```
{
    "msg": "bar"
}
```
