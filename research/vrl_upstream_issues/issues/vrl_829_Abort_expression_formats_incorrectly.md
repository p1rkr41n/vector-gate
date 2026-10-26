# [#829] Abort expression formats incorrectly

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/829)
- **Status**: `OPEN`
- **Author**: [@DylanRJohnston](https://github.com/DylanRJohnston)
- **Created At**: `2024-05-07T07:13:05Z`
- **Updated At**: `2024-05-07T07:15:49Z`
- **Comments**: 0
- **Labels**: _None_
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/829)

---

## Description

Hey all,

I'm currently working on a transpiler from another language into VRL. All other parts of the AST implement Display in a way that is valid syntactically to parse it again i.e. parse <-> display (formatting not withstanding). However the implementation of Display for `abort` incorrectly places a colon in its output.

https://github.com/vectordotdev/vrl/blame/b6fd5ecf3e4d75ccc5a822dcebe8a0fe7d04ef78/src/parser/ast.rs#L1199

The following kind of test succeeds for all other expressions in VRL.

```rs
    #[test]
    fn abort_isomorphism_failure() {
        let expression = r#"abort "error message""#;

        assert_eq!(
            format!("{expression}\n"),
            vrl::parser::parse(expression).unwrap().to_string()
        )
    }
```

I don't know if this kind of isomorphism via `std::fmt::Display` is a guarantee the project is looking to provide, but beyond transpilers it's also very useful for pretty printers since printing from the parsed AST canonicalizes the formatting.
