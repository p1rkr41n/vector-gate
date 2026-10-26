# Issue #562: Unable to pass elements of regular expressions list to function parse_regex_all

- **URL:** https://github.com/vectordotdev/vrl/issues/562
- **Author:** @spacepatcher
- **Status:** CLOSED (completed)
- **Created:** 2023-11-15T16:16:47Z
- **Closed:** 2023-11-21T16:44:12Z
- **Labels:** None

## Description

Hi there!
I have a list of regular expressions exported from an external source. I want to use the function `parse_regex_all` with each of them as a parameter. I'm looking for a way to create a code that follows this logic:
```
regex_list = [
r'pattern1',
r'pattern2'
]

for_each(regex_list) -> |_index, _| {
    .http_status = to_string!(.http_status)

    parse_regex_all!(.http_status, regex_list[_index]) # 1. 
    parse_regex_all!(.http_status, get!(regex_list, [_index])) # 2. 
}
```
I expected the function calls in `1.` or `2.` to be executed without any errors, but in fact, errors have occurred accordingly:
```
error[E203]: syntax error
   ┌─ :11:47
   │
11 │     parse_regex_all!(.http_status, regex_list[_index])
   │                                               ^^^^^^
   │                                               │
   │                                               unexpected syntax token: "Identifier"
   │                                               expected one of: "integer literal"
   │
   = see language documentation at https://vrl.dev
   = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

```
error[E610]: function compilation error: error[E400] unexpected expression type
   ┌─ :13:5
   │
13 │     parse_regex_all!(.http_status, get!(regex_list, [_index]))
   │     ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^
   │     │
   │     unexpected expression for argument "pattern"
   │     expected: regex
   │     received: function call
   │
   = learn more about error code 400 at https://errors.vrl.dev/400
   = see language documentation at https://vrl.dev
   = try your code in the VRL REPL, learn more at https://vrl.dev/examples
```

Would you give me any clues on how to implement the desired logic. Cheers!
