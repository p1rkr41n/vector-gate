# [#146] Add pipe operator support

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/146)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2020-12-07T11:58:03Z`
- **Updated At**: `2026-06-01T14:16:02Z`
- **Comments**: 5
- **Labels**: `vrl:syntax`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/146)

---

## Description

Remap revolves around expressions, most expressions are implemented as functions, which take zero or more input arguments, and provide output.

For example:

```rust
trim(uppercase(to_string(.foo)))
```

The above will eventually (#4905) also work in string templates in Vector itself:

```handlebars
my_config_field = "{{ trim(uppercase(to_string(.foo))) }}"
```

The above works, but can be hard to read.

I wonder if we want to add support for the _pipe operator_ (similar to [Elixir](https://elixirschool.com/en/lessons/basics/pipe-operator/)).

```elixir
.foo |> to_string |> uppercase |> trim
```

```handlebars
my_config_field = "{{ .foo |> to_string |> uppercase |> trim }}"
```

The gist of this syntax would be that given an expression, if the expression is followed by the pipe operator (`|>`), then the expression _after_ that operator would receive the result of the previous expression as its first argument.

The precedence of the pipe operator would be higher than the other operators. This allows one to write:

```elixir
.foo = .bar |> split |> contains("baz") || .baz |> to_string |> contains("qux") # bool

# similar to
.foo = ((.bar |> split |> (contains("baz")) || (.baz |> to_string |> contains("qux"))) # bool
```

You can still supply more arguments if need be:

```elixir
"foo bar,baz" |> split(delimiter = ",") |> join(delimiter = "|") # "foo bar|baz"
```

This would be purely syntactic sugar to make the code easier to read, especially in string templates, but also in general.

---

There are still some design decisions to make (for example, what happens if you provide a non-function expression to the rhs of the pipe operator? Compile error?), but I wanted to put this issue up to gauge interest from others.

Also, some languages that focus specifically on templating use the [`|` pipe syntax to do this](https://tera.netlify.app/docs/#filters):

```elixir
.foo | to_string | uppercase | trim
```

We could do this, but then we'd lose the ability to implement bitwise operators in the future.

cc @binarylogic @FungusHumungus
