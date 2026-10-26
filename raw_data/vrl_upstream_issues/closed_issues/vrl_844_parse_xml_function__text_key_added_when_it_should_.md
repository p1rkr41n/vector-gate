# Issue #844: parse_xml function : text key added when it should not for single nodes

- **URL:** https://github.com/vectordotdev/vrl/issues/844
- **Author:** @ScriptToddler
- **Status:** CLOSED (completed)
- **Created:** 2024-05-18T20:25:24Z
- **Closed:** 2024-10-22T18:28:57Z
- **Labels:** vrl:stdlib

## Description

Hello,

## Problem

There appears to be an inconsistency with `text_key` in `parse_xml` function

Whenever a chain of an "even" number of single child is present, the text key seems to be forcibly added even when it should not.
E.g. : 
- `<root><a>test</a></root>` results in `{ "root": { "a": { "text": "test" } } }` instead of expected `{ "root": { "a": "test" } }`
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLnhtbF9wYXJzZWQgPSBwYXJzZV94bWwhKC5tZXNzYWdlKSIsImV2ZW50Ijp7Im1lc3NhZ2UiOiI8cm9vdD48YT50ZXN0PC9hPjwvcm9vdD4ifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D
- `<root><a><a1>test</a1></a></root>` results in expected `{ "root": { "a": { "a1": "test" } } }`
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLnhtbF9wYXJzZWQgPSBwYXJzZV94bWwhKC5tZXNzYWdlKSIsImV2ZW50Ijp7Im1lc3NhZ2UiOiI8cm9vdD48YT48YTE%2BdGVzdDwvYTE%2BPC9hPjwvcm9vdD4ifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D
- `<root><a><a1><a2>test</a2></a1></a></root>` results in `{ "root": { "a": { "a1": { "a2": { "text": "test" } } } } }` instead of expected `{ "root": { "a": { "a1": { "a2": "test" } } } }`
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLnhtbF9wYXJzZWQgPSBwYXJzZV94bWwhKC5tZXNzYWdlKSIsImV2ZW50Ijp7Im1lc3NhZ2UiOiI8cm9vdD48YT48YTE%2BPGEyPnRlc3Q8L2EyPjwvYTE%2BPC9hPjwvcm9vdD4ifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D
- similarly, if you add a sibling to the `<a>` node, the `<a1>` node then is nested with a text key
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoiLnhtbF9wYXJzZWQgPSBwYXJzZV94bWwhKC5tZXNzYWdlKSIsImV2ZW50Ijp7Im1lc3NhZ2UiOiI8cm9vdD48YT48YTE%2BdGVzdDwvYTE%2BPC9hPjxiPmZvbzwvYj48L3Jvb3Q%2BIn0sImlzX2pzb25sIjpmYWxzZSwiZXJyb3IiOm51bGx9


## Investigation (might be mistaken)

I tried to investigate the issue and it seems to me the problem stems from the recurse implementation with single nodes, and precisely this line https://github.com/vectordotdev/vrl/blob/e58ac8026d98440571ccee46a29e42c1419d6883/src/stdlib/parse_xml.rs#L356
When recursing the value of the node which would then incorrectly add the text key later on at this step (if I am not mistaken) : https://github.com/vectordotdev/vrl/blob/e58ac8026d98440571ccee46a29e42c1419d6883/src/stdlib/parse_xml.rs#L296

The problem seems to be fixed on my end if instead of the recurse, the process_node function is instead called on the node, with no regression seen so far.
I have proposed such a fix on a branch on my forked version of the project there https://github.com/vectordotdev/vrl/compare/main...ScriptToddler:vrl:fix/parse_xml_unique_child_text?expand=1 along with tests highlighting the issue.

I may be mistaken, in which case you may just discard what I said in this last part

Thank you,
