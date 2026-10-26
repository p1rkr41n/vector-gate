# [#911] Support for type widening

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/911)
- **Status**: `OPEN`
- **Author**: [@DylanRJohnston](https://github.com/DylanRJohnston)
- **Created At**: `2024-06-26T02:40:59Z`
- **Updated At**: `2024-07-03T20:43:37Z`
- **Comments**: 5
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/911)

---

## Description

Hey all, I'm currently working on a transpiler from another data processing language to VRL. Unfortunately due to a NDA I can't go into more specifics but a common problem I've encountered is VRL's strict error handling based on type information that is not possible to know at transpilation time.

For example taking a common operator from most other languages

```
static_query += expr
```

the equivalent VRL is

```vrl
static_query = static_query + expr
```

however this often fails to compile due to strict error handling around types, unless both `static_query` and `expr` are known to be integers, this expression can fail, and requires error handling

```vrl
static_query, err = static_query + expr
```

However, you can't just use this in the transpiler as often there are times when the types are well known enough for this expression to not fail, which then causes the compiler to fail as VRL does not allow superfluous error handling. Using type assertions does not work for the same reason.

A workaround I've taken to using is using dead code paths to trick the compiler into widening the type and therefore allowing the superfluous type assertion e.g.

```vrl
if false {
  static_query = null
}
static_query = int!(static_query) + expr
```

However `expr` can also sometimes have a known type, and sometimes not, if `expr` is another static query into the event, it doesn't have a known type, if expr is a literal, or a reference to a variable with a known type it does. Which requires in the most general case something like.


```vrl
static_query = int!({
    tmp = static_query
    if false {
      tmp = null
    }
    tmp
  }) + int!({
    tmp = expr
    if false {
      tmp = null
    }
    tmp
  })
```

As you can see this becomes very noisy very quickly. I was wondering how you'd feel about the introduction of a type assertion that widens types, e.g. `any()` similar to `int()` or `string()`, it would be infailable as it's always safe to map any type to `any` and would help greatly in these cases where the transpiler is needing to output code without enough type information. e.g.

```vrl
static_query = int!(any(static_query)) + int!(any(expr))
```

What do you think?
