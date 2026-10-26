# Issue #5538: Remap will overwrite a map rather than add the field to it

- **URL:** https://github.com/vectordotdev/vector/issues/5538
- **Author:** @StephenWakely
- **Status:** CLOSED (completed)
- **Created:** 2020-12-14T22:20:07Z
- **Closed:** 2021-01-05T14:24:07Z
- **Labels:** domain:vrl

## Description

From the Repl:

```
$ .foo = 3
3

$ .
{ "foo": 3 }

$ .bar = 4
4

$ .
{ "bar": 4 }
```

I would expect when setting `.bar` that it would add that field to the map. It doesn't, it overwrites the entire map.

It should do:

```
$ .foo = 3
3

$ .
{ "foo": 3 }

$ .bar = 4
4

$ .
{ "bar": 4,  "foo": 3 }
```

I believe in the Remap transform, this won't happen with the root object as that is handled differently from `Value::Map` fields. If you try to set the field to any child maps, this will occur.


