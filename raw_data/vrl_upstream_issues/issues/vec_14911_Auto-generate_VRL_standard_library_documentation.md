# [#14911] Auto-generate VRL standard library documentation

- **Repository**: [vectordotdev/vector](https://github.com/vectordotdev/vector/issues/14911)
- **Status**: `OPEN`
- **Author**: [@JeanMertz](https://github.com/JeanMertz)
- **Created At**: `2022-10-21T09:51:49Z`
- **Updated At**: `2022-10-21T09:52:41Z`
- **Comments**: 0
- **Labels**: `domain:external docs`, `domain:vrl`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vector/issues/14911)

---

## Description

As we're working on improving our auto-generated documentation in Vector, we want to do the same for VRL.

The goal is to remove any dependency on Cue for code that we _can_ auto-generate. This means any free-form documentation will stay as-is (e.g. explanation around the [concepts of VRL](https://vrl.dev), etc.). Additionally, we might want to generate [expression documentation](https://vrl.dev/expressions), but that is out-of-scope for the first pass.

The first pass of this work is to auto-generate the [documentation of all of our functions](https://vrl.dev/functions).

The requirements for this issue to be resolved is to **expose the same information exposed through the [`functions.cue` file](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/website/cue/reference/remap/functions.cue), but do so through the [`Function` trait](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/lib/vrl/compiler/src/function.rs#L23-L71)**.

Here's a list of work that needs to be resolved:

- Implement [`Function#summary`](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/lib/vrl/compiler/src/function.rs#L27-L30) for every stdlib function (trait method currently exists, but defaults to `TODO`, has to be written manually, as a single-line description)
- Implement [`Function#usage`](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/lib/vrl/compiler/src/function.rs#L32-L35) for every stdlib function (trait method currently exists, but defaults to `TODO`, has to be replaced with Cue's [`Function#description` field](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/website/cue/reference/remap/functions.cue#L17))
- Add new trait method to `Function` to allow [_notices_](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/website/cue/reference/remap/functions.cue#L18) to be added to functions. We'll likely want to make this a bit more strict than a free-form array of strings, to support the notion of notice severity and title/description separation.
- An enumeration of [function categories](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/website/cue/reference/remap/functions.cue#L16) needs to be introduced and exposed through a new `Function#module` method.
- We need to update the [`Parameter` type](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/lib/vrl/compiler/src/function.rs#L124-L143) to include parameter [descriptions](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/website/cue/reference/remap/functions.cue#L6). These descriptions can be copied over from the existing Cue docs.
- Additionally, but more involved, we want to encode [default values](https://github.com/vectordotdev/vector/blob/79387ae865ec11450bcf052ec02035cf1cc0b077/website/cue/reference/remap/functions.cue#L8) in the `Parameter` type, which we then also want to enforce usage of in the actual function implementation, to avoid drift between parameter defaults and actual defaults used in the function implementation. It's important to note that (ideally) this is _enforced_, not _encouraged_, as best-practices are difficult enough to enforce within a team of engineers, let alone a wider open-source ecosystem of contributors.

Finally, once the above features are in place, we need to **introduce a new `lib/vrl/docs` crate** that iterates all function definitions, and generates a JSON output file similar to what `./scripts/cue.sh export -e remap | jq .functions` would output in the root-level Vector directory.
