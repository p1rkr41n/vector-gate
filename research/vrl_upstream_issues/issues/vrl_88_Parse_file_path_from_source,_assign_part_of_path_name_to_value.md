# [#88] Parse file path from source, assign part of path/name to value

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/88)
- **Status**: `OPEN`
- **Author**: [@DaveWK](https://github.com/DaveWK)
- **Created At**: `2021-10-25T17:00:35Z`
- **Updated At**: `2023-03-28T13:49:06Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/88)

---

## Description

Hi,

I couldn't find an easy way to do this in the docs, but it would be nice to be able to have a VRL function that can parse file paths and allow me to do things like assign values based on a piece of that path. If this is already doable, I imagine this is a fairly common thing to do and an example in the docs would be appreciated.

In example with a "file" source type, assume file is at: /var/log/test/foo.log

then in the transforms:

.service_name = get!(parse_filepath(.file), path: [-1])

should assign service_name to be "foo"

The file parser would be os-agnostic so windows/linux paths get parsed without the user having to worry about things like slashes or "C:\" vs "/"
