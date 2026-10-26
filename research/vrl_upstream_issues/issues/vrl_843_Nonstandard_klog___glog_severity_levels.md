# [#843] Nonstandard klog / glog severity levels

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/843)
- **Status**: `OPEN`
- **Author**: [@srstrickland](https://github.com/srstrickland)
- **Created At**: `2024-05-17T23:16:17Z`
- **Updated At**: `2024-05-20T18:16:48Z`
- **Comments**: 1
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/843)

---

## Description

We have some applications which use klog or glog format with "nonstandard" log levels (generally common, but technically not part of either spec), namely "D" for debug and "T" for trace.  In my parsing code, I can apply VRL workarounds, but I'm wondering what the appetite would be for the 2-line change ([here](https://github.com/vectordotdev/vrl/blob/main/src/stdlib/parse_klog.rs#L16) and [here](https://github.com/vectordotdev/vrl/blob/main/src/stdlib/parse_glog.rs#L16)) to support parsing these?  I'm happy to submit a PR, but I realize it's a bit esoteric and perhaps I should just keep my VRL hack.

```
D0505 17:59:40.692994   28133 klog.go:70] hello from klog  # level = debug
T0505 17:59:40.692994   28133 klog.go:70] hello from klog  # level = trace
```
