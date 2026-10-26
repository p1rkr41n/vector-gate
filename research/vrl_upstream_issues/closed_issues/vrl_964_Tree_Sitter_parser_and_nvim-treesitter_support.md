# Issue #964: Tree Sitter parser and nvim-treesitter support

- **URL:** https://github.com/vectordotdev/vrl/issues/964
- **Author:** @belltoy
- **Status:** CLOSED (completed)
- **Created:** 2024-07-31T01:28:58Z
- **Closed:** 2025-06-18T02:31:41Z
- **Labels:** domain:dev

## Description

I'm using and following vector for years. There is a missing part since the VRL was introduced till now, the syntax support in editors. I found some people were trying to build tree-sitter parse few years ago but not finished at the end.

Earlier, I've written a simple [vim plugin](https://github.com/belltoy/vrl.vim) via the original vim syntax match to highlight VRL codes. But that's not good enough for the modern develop environment.

Recently, I wrote a [VRL parser](https://github.com/belltoy/tree-sitter-vrl) and integrated it into [neovim](https://github.com/nvim-treesitter/nvim-treesitter).

Finally, we have a better syntax highlighting and something more provided by the power of tree-sitter, such as **code folding**, **auto indentation**, **variable references**, and **code injections** in YAML/TOML files. Other editor than neovim could be easily adding VRL support via tree-sitter support.

Hope that helps.
