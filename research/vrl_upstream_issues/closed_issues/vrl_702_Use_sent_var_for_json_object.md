# Issue #702: Use sent var for json object

- **URL:** https://github.com/vectordotdev/vrl/issues/702
- **Author:** @morgoved
- **Status:** CLOSED (completed)
- **Created:** 2024-02-15T21:57:12Z
- **Closed:** 2024-02-15T23:10:05Z
- **Labels:** None

## Description

So i have for example this input

```
{
    "log": {
        "file": "/var/log/pods/test_brain-zookeeper-0_3c9fcca1-ed6b-4ef8-910a-f3c6e5ec99c7/brain-zookeeper/0.log",
        "kubernetes": {
            "container_id": "containerd://cc4f87f446527dd8736ded9eab529ea3dc7a7d4bc9e1a61e34c0583421093f9c",
            "container_image": "wurstmeister/zookeeper",
            "container_image_id": "docker.io/wurstmeister/zookeeper@sha256:7a7fd44a72104bfbd24a77844bad5fabc86485b036f988ea927d1780782a6680",
            "container_name": "brain-zookeeper",
            "namespace_labels": {
                "kubernetes.io/metadata.name": "test"
            },
            "node_labels": {
                "beta.kubernetes.io/arch": "amd64",
                "beta.kubernetes.io/os": "linux",
                "kubernetes.io/arch": "amd64",
                "kubernetes.io/hostname": "appdev-1",
                "kubernetes.io/os": "linux",
                "node": "test",
                "node-role.kubernetes.io/worker": "worker"
            },
            "pod_annotations": {
                "cni.projectcalico.org/containerID": "ce640500fdd0086dd849f09978337fc60d2a6bcec13de1bfc895142d835026f3",
                "cni.projectcalico.org/podIP": "10.244.17.203/32",
                "cni.projectcalico.org/podIPs": "10.244.17.203/32"
            },
            "pod_ip": "10.244.17.203",
            "pod_ips": [
                "10.244.17.203"
            ],
            "pod_labels": {
                "app": "brain-zookeeper",
                "controller-revision-hash": "brain-zookeeper-6b5fd9d454",
                "node": "test",
                "statefulset.kubernetes.io/pod-name": "brain-zookeeper-0",
                "tier": "brain-zookeeper"
            },
            "pod_name": "brain-zookeeper-0",
            "pod_namespace": "test",
            "pod_node_name": "appdev-1",
            "pod_owner": "StatefulSet/brain-zookeeper",
            "pod_uid": "3c9fcca1-ed6b-4ef8-910a-f3c6e5ec99c7"
        },
        "message": {
            "level": "info",
            "ID": "e8f58963-2775-4238-91ae-13b03efb4559",
            "time": 1708015591742297,
            "message": "<-- IP: 10.10.10.1 GET /self/settings 200 1 ms"
        },
        "source_type": "kubernetes_logs",
        "stream": "stdout",
        "timestamp": "2024-02-15T12:40:04.616543848Z"
    }
}
```

and i need get 

this

```
{
    "env": "test",
    "ID": "34994eef-3cfc-4c93-91ab-bfd998f9b2f8",
    "level": "info",
    "message": "--> IP: 10.10.10.1 GET /self"
    "pod_name": "api-59677d9489-vg9kg",
    "timestamp": "2024-02-15T20:55:44.469929813Z"
}
```

but message can have dinamic json keys

and i try use this approach

```
              source: |-
                # unescaped_message = replace(.message, "/\", "" )
                # . = .| parse        
                parse_kuber = parse_json(.kubernetes) ?? {}
                parsed_message = parse_json(.message) ?? {}
                . = parsed_message
                .container_image = parse_kuber.container_image
                .env = parse_kuber.pod_namespace
                .pod_name = parse_kuber.pod_name
                del(.time)
```

But 
just have for example this 

```
{
    "ID": "23e845f3-879c-48e9-9146-bd0e992c24de",
    "container_image": null,
    "env": null,
    "level": "info",
    "message": "--> IP: 10.10.10.1 GET /self/settings",
    "pod_name": null
}
```
i tryed use this before 
parsed_message = parse_json(.message) ?? {}
container_image  = .log.kubernetes.container_image
.container_image = container_image  

but it get container_image as null.

how i can do this?


