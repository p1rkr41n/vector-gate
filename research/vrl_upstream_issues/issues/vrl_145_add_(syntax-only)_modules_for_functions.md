# [#145] add (syntax-only) modules for functions

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/145)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2020-12-11T20:31:37Z`
- **Updated At**: `2023-03-28T14:37:03Z`
- **Comments**: 5
- **Labels**: `type:enhancement`, `vrl:syntax`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/145)

---

## Description

Now that we're cranking out more and more functions, I'm worried it'll become more difficult to know the distinction between all of them.

Take for example the newly proposed [`to_level`](https://github.com/timberio/vector/pull/5503) and [`to_severity`](https://github.com/timberio/vector/pull/5505). On their own, they make total sense, but when you put them next to `to_string`, `to_int` and the other `to_*` functions that convert to a concrete value, they can be confusing.

A similar situation arises with functions such as [`parse_aws_vpc_flow`](https://github.com/timberio/vector/pull/5504) and [`parse_aws_elb`](https://github.com/timberio/vector/pull/5489).

We've already started categorizing the functions in our Cue documentation precisely because the list of functions is becoming longer still, and you need some way to more easily find what you're looking for.

I propose we extend this categorization to the language itself, by introducing _function modules_.

The concept is simple:

1. We define a new `Module` enum that has variants such as `Root`, `Aws`, `Syslog`, and more.
2. We update our `Function` trait to include a `fn module(&self) -> Module` function.
3. All function implementations are updated to define their module.
4. We update the parser to read function modules and convert them to syntax
5. Users now write `syslog::to_level(.foo)`, or `aws::parse_vpc_flow(.bar)` instead.
6. Functions assigned the `Root` module will stay as-is, so you'd still use `to_int`, `parse_json`, and other often-used functions.

I'll leave it as an exercise to others to come up with the correct module names (I think the Cue files are a good starting point, and I'm sure @lucperkins has some good ideas for this list as well), but I do believe this would only add a _small amount_ of syntactic noise to the language (especially since the most commonly used functions won't have a module prefix), while gaining a bit more structure in the ever-growing list of functions.

_(note I used `<module>::<ident>` since it doesn't collide with other syntax we currently have, and it's also what I'm used to as a Rustacean (and it's not uncommon in other languages either), but we can entertain other forms of syntax for this)_

cc: @binarylogic @FungusHumungus 
