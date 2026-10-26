# Issue #337: Benchmark vs Flink

- **URL:** https://github.com/vectordotdev/vrl/issues/337
- **Author:** @yuzhichang
- **Status:** CLOSED (completed)
- **Created:** 2023-07-19T10:23:17Z
- **Closed:** 2023-07-21T19:00:08Z
- **Labels:** None

## Description

I'm evaluating if Vector remap perform better than Flink on ordinary fields extracting/renaming of JSON record.

Kafka cluster consists of 3 node on seperate machines.
Soure and sink topics are all 3-partitions.
Vector version: 1.31.0, runs on one node of the Kafka cluster.
Flink version: 1.12, runs on other place.  I developed the JSON transform in pure Java. 

| | Thought(events/second)| CPU | Memory|
|---|-----|----|-----|
| Vector | 52K(reported by `vector top`) | 7 vcpu| 900MB |
| Fink | 39K(reported by Grafana) | 1.3 vcpu | 200MB |


My vector config is:
```
[api]
enabled = true

[sources.pod2_source]
type = "kafka"
bootstrap_servers = "192.168.101.94:9092,192.168.101.96:9092,192.168.101.98:9092"
topics = [ "pod_metric" ]
group_id = "vector_pod23"
auto_offset_reset = "smallest"
decoding.codec = "json"

[transforms.pod2_transform]
type = "remap"
inputs = [ "pod2_source" ]
drop_on_abort = true
drop_on_error = true
reroute_dropped = true
metric_tag_values = "single"
source = """
msg = parse_json!(string!(.message))
msg."k8s.cluster.name" = msg.metric.cluster_id
msg."k8s.node.name" = msg.metric.node
msg."k8s.namespace.name" = msg.metric.namespace
msg."k8s.pod.ip" = split!(msg.metric.instance, ":", 2)[0]
msg."k8s.pod.name" = msg.metric.pod_name
msg.__name__ = msg.metric.__name__
msg.timestamp = to_timestamp!(msg.value[0])
msg.value = to_float!(msg.value[1])
msg.__object_id__ = seahash(join!([msg."k8s.cluster.name", msg."k8s.pod.ip"], ", "))
del(msg.metric)
. = msg
"""
timezone = "local"

[sinks.pod2_sink]
type = "kafka"
inputs = [ "pod2_transform" ]
bootstrap_servers = "192.168.101.94:9092,192.168.101.96:9092,192.168.101.98:9092"
compression = "none"
encoding.codec = "json"
topic = "pod_metric_ok"
key_field = "k8s.pod.ip"

[sinks.pod2_sink2]
type = "kafka"
inputs = [ "pod2_transform.dropped" ]
bootstrap_servers = "192.168.101.94:9092,192.168.101.96:9092,192.168.101.98:9092"
compression = "none"
encoding.codec = "json"
topic = "pod_metric_dropped"
```


An example source Json record is:
```
{
	"host": "leno",
	"message": "{\"metric\":{\"container\":\"dcsp-mid-midbu\",\"image\":\"21.33.12.47/dcsp-spec1/dcsp-mid-midbu@sha256:4d5af5d3df7853326a6b871c2fcdd497534b787cda67894694ed38db7568e79f\",\"instance\":\"21.33.30.114:10250\",\"pod\":\"dcsp-mid-midbu-77744c7558-mwgkj\",\"metrics_path\":\"/metrics/cadvisor\",\"pod_name\":\"dcsp-mid-midbu-77744c7558-mwgkj\",\"node\":\"k8phyzlb01w09\",\"cluster_id\":\"k8-phyzl-b01\",\"endpoint\":\"https-metrics\",\"container_name\":\"dcsp-mid-midbu\",\"__name__\":\"pod_memory_usage\",\"service\":\"kubelet\",\"name\":\"k8s_dcsp-mid-midbu_dcsp-mid-midbu-77744c7558-mwgkj_dcsp-spec1-bu02_5d33b581-3ba6-4421-b00f-9c0c267b6523_0\",\"namespace\":\"dcsp-spec1-bu02\",\"id\":\"/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod5d33b581_3ba6_4421_b00f_9c0c267b6523.slice/docker-c93101381553f2e2d8d895bf3fc1fc75f934b030af6858f003baee74987f7bd6.scope\",\"prometheus\":\"monitoring/k8s\",\"job\":\"kubelet\"},\"value\":[1677828485.757,\"21.69208526611328\"]}",
	"source_type": "stdin",
	"timestamp": "2023-07-11T10:02:05.847397443Z"
}
```

An example sink Json record is:
```
{
	"__name__": "pod_cpu_usage",
	"__object_id__": 7642464300114087328,
	"k8s.cluster.name": "k8-phyzl-b01",
	"k8s.namespace.name": "dcsp-spec1-bu06",
	"k8s.node.name": "k8phyzlb01w05",
	"k8s.pod.ip": "21.33.30.61",
	"k8s.pod.name": "dcsp-dcf-serverbu-655954c97-zf8cz",
	"timestamp": "2023-03-03T07:32:12.513000011Z",
	"value": 0.3450426123877763
}
```

I'm surprised with the test result. I assumed Vector will win since Vrl is compiled to native code, Any thoughts?

