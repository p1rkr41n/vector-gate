# [#20] [Web Playground] Make `log()` function wasm compatible

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/20)
- **Status**: `OPEN`
- **Author**: [@jonathanpv](https://github.com/jonathanpv)
- **Created At**: `2022-10-03T21:06:02Z`
- **Updated At**: `2026-06-16T13:10:40Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:log`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/20)

---

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment
<!-- Thank you for keeping this note for the community -->


### Problem

Currently the log function in VRL stdlib doesn't print out anything @fuchsnj believes this is because the log gets sent to nothing due to wasm compilation . 

<img width="1057" alt="image" src="https://user-images.githubusercontent.com/44036128/193678369-0718bc6a-45d6-4b28-a7ec-86999fcab379.png">

Possible way to fix this would be to add an extern call to the log function for console.log(). 

ref: vectordotdev/vector#14654
ref: vectordotdev/vrl#22
