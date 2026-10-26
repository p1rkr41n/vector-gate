# [#136] New `parse_<framework>` Remap functions (niche log parsing)

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/136)
- **Status**: `OPEN`
- **Author**: [@binarylogic](https://github.com/binarylogic)
- **Created At**: `2021-01-21T02:59:41Z`
- **Updated At**: `2026-06-01T14:16:17Z`
- **Comments**: 6
- **Labels**: `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/136)

---

## Description

I wanted to open this issue to see where we land on a solution since these types of parsing problems raise a few interesting questions. Parsing framework logs, like Rails, cuts deeper into the real-world observability problems and we will need to solve this elegantly in the near future.

## Examples

For example, let's use Rails. Rails production logs look like this:

```
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- : Started POST "/articles" for 127.0.0.1 at 2018-06-27 15:48:10 +0000
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- : Processing by ArticlesController#create as HTML
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- :   Parameters: {"utf8"=>"✓", "article"=>{"title"=>"Create New Post", "text"=>"Description for new post"}, "commit"=>"Save Article"}
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- :   [1m[35m (0.2ms)[0m  [1m[35mBEGIN[0m
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- :   ↳ app/controllers/articles_controller.rb:20
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- :   [1m[36mArticle Create (1.0ms)[0m  [1m[32mINSERT INTO "articles" ("title", "text", "created_at", "updated_at") VALUES ($1, $2, $3, $4) RETURNING "id"[0m  [["title", "Create New Post"], ["text", "Description for new post"], ["created_at", "2018-06-27 15:48:11.116208"], ["updated_at", "2018-06-27 15:48:11.116208"]]
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- :   ↳ app/controllers/articles_controller.rb:20
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- :   [1m[35m (0.5ms)[0m  [1m[35mCOMMIT[0m
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- :   ↳ app/controllers/articles_controller.rb:20
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- : Redirected to http://localhost:3000/articles/29
I, [2016-01-26T23:21:44.581108 #27447]  INFO -- : Completed 302 Found in 25ms (ActiveRecord: 4.5ms)
```

## Problem

Parsing these logs is not a fun endeavor:

1. You must unwrap the log with a custom Ruby prefix to extract the level, timestamp, and pid.
1. Custom Regexes will need to be written for lines that allow it.
1. A custom key/value parser is needed for the Ruby stringified parameters. (`{"utf8"=>"✓",...`)
1. ANSI stripping will be required on some lines.
1. Control flow would help to match on each line in order to apply the appropriate parsing strategy. This will help with performance.
1. I'm probably missing some steps.

## Proposal

This is the kind of problem Vector should make easy. I realize this is a very specific version of this problem, but we should think about how we can reduce the pain here.

### Proposal 1: Do nothing

We could decide to not handle these formats and tell users to:

1. Structure your logs at the app level using JSON or some other format.
   1. Note: Vector is sometimes used by operators that do not control the app and therefore can't update the app to structure its logs.
2. Use Grok, since patterns [already exist](https://gist.github.com/paulRbr/b8b31b769fc8c4039034#file-rails).
   1. Note: this is slower and these formats appear to be community managed, so their quality is questionable.
3. Write custom regexes.

### Proposal 2: Add a single `parse_rails` function

This function would perform format detection and return structured logs with a key that users can match on to determine the log type. One simple function call would handle it all.

This offers the best user experience but shifts a lot of tedious responsibility on us, especially since these formats can change across Rails versions.

### Proposal 3: Add multiple `parse_rails_*` functions

`parse_rails_request_start`, `parse_rails_controller`, `parse_rails_sql`, etc, etc.

I don't like this option but wanted to list it to be comprehensive.

### Proposal 4: Community managed Remap functions/formats

Delegate all of this to the community and let them manage this through a number of ways:

1. Community managed Remap functions.
2. Community managed patterns.
3. Community managed components (config macros).

## Final thoughts

I don't particularly like any of these solutions, but I feel like this would be best solved with some sort of community approach if we could control quality.

