# Issue #322: parse_json deosn't work

- **URL:** https://github.com/vectordotdev/vrl/issues/322
- **Author:** @yuzhichang
- **Status:** CLOSED (completed)
- **Created:** 2023-07-13T04:39:40Z
- **Closed:** 2023-07-13T16:08:19Z
- **Labels:** None

## Description

I have another question on `parse_json`.

Background:
Vector version 0.30.0, 0.31.0
Events in Kafka topic look like:

```
{
	"host": "leno",
	"message": "{\"metric\":{\"container\":\"dcsp-mid-midbu\",\"image\":\"21.33.12.47/dcsp-spec1/dcsp-mid-midbu@sha256:4d5af5d3df7853326a6b871c2fcdd497534b787cda67894694ed38db7568e79f\",\"instance\":\"21.33.30.114:10250\",\"pod\":\"dcsp-mid-midbu-77744c7558-mwgkj\",\"metrics_path\":\"/metrics/cadvisor\",\"pod_name\":\"dcsp-mid-midbu-77744c7558-mwgkj\",\"node\":\"k8phyzlb01w09\",\"cluster_id\":\"k8-phyzl-b01\",\"endpoint\":\"https-metrics\",\"container_name\":\"dcsp-mid-midbu\",\"__name__\":\"pod_memory_usage\",\"service\":\"kubelet\",\"name\":\"k8s_dcsp-mid-midbu_dcsp-mid-midbu-77744c7558-mwgkj_dcsp-spec1-bu02_5d33b581-3ba6-4421-b00f-9c0c267b6523_0\",\"namespace\":\"dcsp-spec1-bu02\",\"id\":\"/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod5d33b581_3ba6_4421_b00f_9c0c267b6523.slice/docker-c93101381553f2e2d8d895bf3fc1fc75f934b030af6858f003baee74987f7bd6.scope\",\"prometheus\":\"monitoring/k8s\",\"job\":\"kubelet\"},\"value\":[1677828485.757,\"21.69208526611328\"]}",
	"source_type": "stdin",
	"timestamp": "2023-07-11T10:02:05.847397443Z"
}
```

Vector config file:

```
[sources.pod2_source]
type = "kafka"
bootstrap_servers = "192.168.101.94:9092,192.168.101.96:9092,192.168.101.98:9092"
topics = [ "pod_metric" ]
group_id = "vector_pod2"

[transforms.pod2_transform]
type = "remap"
inputs = [ "pod2_source" ]
drop_on_abort = true
drop_on_error = true
reroute_dropped = true
metric_tag_values = "single"
source = """
msg = parse_json!(string!(.message))
log(msg)
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

The vector output:
```
2023-07-13T03:04:41.829230Z  INFO transform{component_kind="transform" component_id=pod2_transform component_type=remap component_name=pod2_transform}: vrl::stdlib::log: {"host":"leno","message":"{\"metric\":{\"container\":\"dcsp-mid-midbu\",\"image\":\"21.33.12.47/dcsp-spec1/dcsp-mid-midbu@sha256:4d5af5d3df7853326a6b871c2fcdd497534b787cda67894694ed38db7568e79f\",\"instance\":\"21.33.30.145:10250\",\"pod\":\"dcsp-mid-midbu-5f7c5c9bcf-gl925\",\"metrics_path\":\"/metrics/cadvisor\",\"pod_name\":\"dcsp-mid-midbu-5f7c5c9bcf-gl925\",\"node\":\"k8phyzlb01w15\",\"cluster_id\":\"k8-phyzl-b01\",\"endpoint\":\"https-metrics\",\"container_name\":\"dcsp-mid-midbu\",\"__name__\":\"pod_cpu_usage\",\"service\":\"kubelet\",\"name\":\"k8s_dcsp-mid-midbu_dcsp-mid-midbu-5f7c5c9bcf-gl925_dcsp-spec1-bu03_66a3948b-2b9f-4b00-a8fa-740091230129_0\",\"namespace\":\"dcsp-spec1-bu03\",\"id\":\"/kubepods.slice/kubepods-burstable.slice/kubepods-burstable-pod66a3948b_2b9f_4b00_a8fa_740091230129.slice/docker-dfc547dea28858374ba6ef194ea77989dd163cfcd04be07b5301fffd8f8466fa.scope\",\"prometheus\":\"monitoring/k8s\",\"job\":\"kubelet\"},\"value\":[1677828666.669,\"1.069477013669307\"]}","source_type":"stdin","timestamp":"2023-07-11T10:08:29.069551056Z"} internal_log_rate_secs=1 vrl_position=37
```

Run similar script in vrl shell:
```
$ . = {"host":"leno","message":"{\"metric\":{\"cluster_id\":\"k8-phyzl-b01\",\"pod\":\"dcsp-dcf-serverbu-6f7f8dc74b-2sdbj\",\"__name__\":\"pod_filesystem_usage\",\"namespace\":\"dcsp-spec1-bu01\"},\"value\":[1677828783.807,\"0.00977301845002288\"]}","source_type":"stdin","timestamp":"2023-07-11T10:04:48.745189657Z"}
$ parse_json!(string(.message))                                                                                                                                     
{ "metric": { "__name__": "pod_filesystem_usage", "cluster_id": "k8-phyzl-b01", "namespace": "dcsp-spec1-bu01", "pod": "dcsp-dcf-serverbu-6f7f8dc74b-2sdbj" }, "value": [1677828783.807, "0.00977301845002288"] }
```

Question:
The output indicates that `msg` equals to `.` instead of decoded `.message`. This behavor doesn't match with the vrl schell.


