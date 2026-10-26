# [#1539] Update `parse_aws_vpc_flow_log` to version 7 of the VPC flow logs

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1539)
- **Status**: `OPEN`
- **Author**: [@istimaldar](https://github.com/istimaldar)
- **Created At**: `2025-10-14T19:45:01Z`
- **Updated At**: `2026-06-01T14:08:44Z`
- **Comments**: 5
- **Labels**: `vrl:stdlib`, `stdlib:parse_aws_vpc_flow_log`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1539)

---

## Description

### A note for the community

_No response_

### Problem

I'm trying to parse VPC flow logs of version 7. To achieve that, I'm using this function:
```vrl
parse_aws_vpc_flow_log(.message, "version account_id interface_id srcaddr dstaddr srcport dstport protocol packets bytes start end action log_status ecs_cluster_arn ecs_cluster_name ecs_container_instance_arn ecs_container_instance_id ecs_container_id ecs_second_container_id ecs_service_name ecs_task_definition_arn ecs_task_arn ecs_task_id")
```
Which fails with the following error: `function call error for \"parse_aws_vpc_flow_log\" at (16:359): unknown key: ecs_cluster_arn`. 

I think it may be because the current version of `parse_aws_vpc_flow_log` does not support [VPC Flow Logs Version 7](https://docs.aws.amazon.com/vpc/latest/userguide/flow-log-records.html#flow-logs-fields).


Here is the minimal example to reproduce the issue on [VRL playground](https://playground.vrl.dev/):

### Input
```json
{
    "message": "7 001607371330 eni-0ef0daf8c5366185a 18.142.59.252 10.195.1.73 29353 34686 6 1 52 1760469769 1760469799 ACCEPT OK security-operation-services-ecs arn:aws:ecs:eu-west-1:001607371330:cluster/security-operation-services-ecs - - prod-security-bo-be arn:aws:ecs:eu-west-1:001607371330:task-definition/prod-wptg-player-report:10 de2b6f1419544b8cb9696ce997eb6804 arn:aws:ecs:eu-west-1:001607371330:task/security-operation-services-ecs/de2b6f1419544b8cb9696ce997eb6804 de2b6f1419544b8cb9696ce997eb6804-2045100114 -"
}
```

### VRL Program

```text
message, .err = parse_aws_vpc_flow_log(.message, "version account_id interface_id srcaddr dstaddr srcport dstport protocol packets bytes start end action log_status ecs_cluster_arn ecs_cluster_name ecs_container_instance_arn ecs_container_instance_id ecs_container_id ecs_second_container_id ecs_service_name ecs_task_definition_arn ecs_task_arn ecs_task_id")
if (.err == null) {
    . = message
}
```

### VRL and/or Vector Version

vector 0.50.0 (x86_64-unknown-linux-gnu)

### Debug Output

```text
function call error for \"parse_aws_vpc_flow_log\" at (16:359): unknown key: `ecs_cluster_arn`
```

### Example

_No response_

### Additional Context

_No response_

### References

_No response_
