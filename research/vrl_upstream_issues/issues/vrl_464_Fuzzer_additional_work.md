# [#464] Fuzzer additional work

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/464)
- **Status**: `OPEN`
- **Author**: [@pront](https://github.com/pront)
- **Created At**: `2023-09-19T21:36:29Z`
- **Updated At**: `2023-09-28T13:49:26Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `fuzz`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/464)

---

## Description

```[tasklist]
### Tasks
- [ ] Fix [bugs](https://github.com/vectordotdev/vrl/issues?q=is%3Aopen+is%3Aissue+label%3Afuzz) discovered by the fuzzer
- [ ] Add more seeds/inputs.
- [ ] Identify known failures and ignore them so that we can keep discovering new bugs.
- [ ] On failure, the fuzzer will provide the input that caused a failure. We can improve this error report to reduce debugging time. A simple idea is to re-evaluate the VRL failed program.
- [ ] Add a Github workflow that runs the fuzzer X times/week for Y hours/run.
- [ ] (Optional) Automatically open Github issues for newly discovered bugs. This requires assigning IDs to failures.
```

The above list is not exhaustive but a good starting point.
