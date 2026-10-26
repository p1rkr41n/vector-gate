# [#458] Explore support for a native code transform 

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/458)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2023-09-18T19:14:32Z`
- **Updated At**: `2026-06-01T14:18:19Z`
- **Comments**: 0
- **Labels**: `vrl:compiler`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/458)

---

## Description

The following is not a formal proposal/design but just an idea that could be explored in the future.
 
Today Vector supports the [Lua transform](https://vector.dev/docs/reference/configuration/transforms/lua/). This issue is a suggestion to explore something similar for native code either as part of VRL or standalone. I am adding this issue as placeholder for potential future work.


Let's use string manipulation as a motivating example.

Imagine a user wants to determine whether a string contains all the following substrings ["abc", "xyz"]. This can be done today by using multiple VRL functions and combining their results. See the following VRL snippet:

```
sentence = "A needle in the haystack"
contains_needle = contains(sentence, "needle")
contains_haystack = contains(sentence, "haystack")
contains_both = contains_needle && contains_haystack

if contains_both {
    # do A
} else {
    # do B
}
```

If VRL had a transform that supported Rust code it would look like:
```
sentence = "A needle in the haystack"
contains_both = contains_all_native(sentence, "needle", "haystack")

if contains_both {
    # do A
} else {
    # do B
}
```

This allows for tremendous flexibility and reduces engineering efforts since we don't need to introduce a new VRL function for each string manipulation that needs optimization.

Note that the user would also need to implement `contains_all_native` and that would need to be compiled first and then invoked. There are several unanswered design questions here. 
