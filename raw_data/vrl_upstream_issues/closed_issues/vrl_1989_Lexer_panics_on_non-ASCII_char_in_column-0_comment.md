# Issue #1989: Lexer panics on non-ASCII char in column-0 comment inside a block ("is not a char boundary", lex.rs:923)

- **URL:** https://github.com/vectordotdev/vrl/issues/1989
- **Author:** @heresie
- **Status:** CLOSED (completed)
- **Created:** 2026-10-12T09:37:26Z
- **Closed:** 2026-10-16T18:42:20Z
- **Labels:** vrl:compiler

## Description

## Description

Since VRL 0.36.0 (shipped in Vector 0.59.0), the lexer panics on a valid program that contains a non-ASCII character in a comment. The same program compiles and runs fine on VRL 0.35.0 / Vector 0.58.0.

```
thread 'main' panicked at vrl-0.36.0/src/parser/lex.rs:923:47:
start byte index 35 is not a char boundary; it is inside '—' (bytes 34..37 of string)
```

In Vector this makes `vector validate` / `vector test` panic, and a config containing such a `remap` transform crashes the whole topology at startup.

## Reproduction

`repro.vrl`:

```coffee
x = {}
if !is_object(x) {
# a
# b — c
  .a = 1
}
.a
```

```sh
docker run --rm -v $PWD:/w timberio/vector:0.58.0-alpine vrl --input /dev/null --program /w/repro.vrl
# null

docker run --rm -v $PWD:/w timberio/vector:0.59.0-alpine vrl --input /dev/null --program /w/repro.vrl
# thread 'main' panicked at .../vrl-0.36.0/src/parser/lex.rs:923:47:
# start byte index 35 is not a char boundary; it is inside '—' (bytes 34..37 of string)
```

Observations:
- At least two consecutive comment lines are needed, and they must start at column 0. Indenting them makes the panic go away.
- The non-ASCII character must be in the second comment.
- With an ASCII-only second comment, there is no panic.

## Analysis

`delimited_query_char` (introduced in 2cc1119, "chore(lints): remove parser pedantic exceptions (#1946)") slices the input before checking which character is at `pos`:

```rust
let mut lexer = Lexer::new(&self.input[pos + 1..]);   // lex.rs:923
let (result, description) = if input.starts_with('"') {
    ...
} else {
    return Ok(chars.peek().expect("query character is present").1);
};
```

`pos + 1` is only a valid char boundary when the character at `pos` is ASCII. Before #1946, the `Lexer::new(&self.input[pos + 1..])` calls were inside the `'"'`/`s'`/`r'`/`t'` branches, so they only ever ran after a single-byte character.

A non-ASCII character reaches this code because of how comments are skipped in the delimited-query scan. The `#` branch consumes the first comment up to and including `\n`. The caller then calls `chars.next()`, which eats the `#` of the next comment as an ordinary character. The rest of that comment line is then scanned char by char, and the first multi-byte character panics.

So there are probably two issues:
1. **Panic:** the slice should move into the branches that need it, or `pos + ch.len_utf8()` should be used.
2. **Comment handling:** a comment directly after another comment at column 0 isn't recognised as a comment during this lookahead. This is harmless for ASCII, but it is still incorrect.

The code is unchanged on current `main`.

## Versions

- Vector 0.59.0 (`timberio/vector:0.59.0-alpine`), VRL 0.36.0: panics
- Vector 0.58.0 (`timberio/vector:0.58.0-alpine`): OK
