# Issue #704: Add "sieve" string function

- **URL:** https://github.com/vectordotdev/vrl/issues/704
- **Author:** @johnhtodd
- **Status:** CLOSED (completed)
- **Created:** 2024-02-19T03:39:37Z
- **Closed:** 2024-03-11T23:10:35Z
- **Labels:** vrl:stdlib

## Description

It would be useful to have a method to remove characters from strings which are undesired or un-necessary for parsing of data (typically distilling to human-readable data fields.)  This would eliminate or replace characters that have special (dangerous) meaning to downstream consumers, or which are not presentable in other formats. 

Purposes for this function are multiple: it provides an additional layer of safety for downstream systems which may not handle characters appropriately; it may reduce the volume of data where there are large numbers of unprintable or unstructured characters in a message; it may make more readable certain messages that contain excessive numbers of extraneous characters.

I would propose the function name of "sieve" for this function, and at first glance I would imagine three arguments:

  - string to act upon (required)
  - set of characters to permit, in example form:   [A-z],[0-9], \,, ü, 0xE282AC  (required) 
     - this would be ranges of ASCII or UTF-8 
     - actual characters embedded in config file (is this legal in Vector configs?)
     - hexadecimal UTF-8 
     - escaped (\) special characters
  - character to insert/overwrite single instances of deleted results in output (default is to delete all characters other than sieve list.) Can be explicitly set to "" to delete characters with no replacement. (optional)
  - character to insert/overwrite when two or more sequential instances of deleted characters are in input string. Can be explicitly set to "" to delete characters with no replacement. (optional)
  
