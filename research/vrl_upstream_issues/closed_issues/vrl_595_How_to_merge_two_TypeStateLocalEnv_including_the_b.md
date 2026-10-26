# Issue #595: How to merge two `TypeState`/`LocalEnv` including the `bindings`? 

- **URL:** https://github.com/vectordotdev/vrl/issues/595
- **Author:** @dotansimha
- **Status:** CLOSED (completed)
- **Created:** 2023-12-12T16:59:32Z
- **Closed:** 2023-12-14T13:20:39Z
- **Labels:** meta:confirmed

## Description

My use case for VRL is to allow multiple `Program`s to run serially, and I have a shared `RuntimeState` that allows me to share the runtime state. 
I also want to allow variables to be shared across `Program`s. To do that, I'm using `compile_with_state` and passing the previous state. But in the case of >2 `Program`s, I need to merge the `TypeState` of multiple `Program`s. 

```
# Program 1: this one works obviously
my_var1 = "1"

# Program 2: this one also works, because I only need to use a single TypeState (from program 1)
my_var2 = "2"
log("my_var1: " + my_var1 + "my_var2: " + my_var2);

# Program 3: This one fails because "merge" doesn't work as expected
log("my_var1: " + my_var1 + "my_var2: " + my_var2);
```

I tried to use the `LocalEnv::merge` function, but it seems like it's merging the `details` only, without merging the `bindings` vector together:
https://github.com/vectordotdev/vrl/blob/59fb310809ac7bb9f2e1b137d10ca4178a4e5625/src/compiler/state.rs#L87-L93

I suspect that `LocalEnv::merge` might have a bug because it does not merge the complete `bindings` vectors. I tried to work around it but it seems like all functions and properties are `pub(crate)` so I can't seem to create the `LocalEnv` manually with the data I need. 
I created a PR to address this issue: https://github.com/vectordotdev/vrl/pull/596
