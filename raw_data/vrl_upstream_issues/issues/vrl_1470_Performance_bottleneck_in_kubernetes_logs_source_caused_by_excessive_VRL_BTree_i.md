# [#1470] Performance bottleneck in kubernetes_logs source caused by excessive VRL BTree insert operations

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1470)
- **Status**: `OPEN`
- **Author**: [@huanghuangzym](https://github.com/huanghuangzym)
- **Created At**: `2025-08-08T09:14:21Z`
- **Updated At**: `2025-08-12T18:06:01Z`
- **Comments**: 4
- **Labels**: `domain:performance`, `domain:core`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1470)

---

## Description

**Describe the performance issue**
When using the `kubernetes_logs` source, we observed significantly lower log ingestion throughput compared to the `file` source.

* **Same environment (HDD storage)**:

  * `file` source: \~120k events/sec
  * `kubernetes_logs` source: \~30k events/sec

During profiling, we found that a large amount of CPU time is spent in **VRL `BTree` insert operations** inside the metadata enrichment process.

---

**To Reproduce**

1. Deploy Vector as a DaemonSet using `kubernetes_logs` source.
2. Generate high log throughput from multiple busy-looping pods.
3. Monitor ingestion performance.
4. Compare with a configuration using the `file` source directly reading `/var/log/containers/...`.
5. Run `perf` or similar profiler; observe hotspots in:

   ```
   vrl::value::value::crud::insert::insert
   ```

---

**Expected behavior**
The `kubernetes_logs` source should have ingestion throughput closer to the `file` source.
Metadata enrichment should not become the dominant CPU bottleneck at high event rates.

---


**Proposed optimization ideas**

* Evaluate alternative map implementations (`HashMap` or specialized small-map data structures) for VRL values.





