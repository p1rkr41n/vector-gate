# Issue #263: bug: parse_aws_vpc_flow_log types account-id as int64 instead of string

- **URL:** https://github.com/vectordotdev/vrl/issues/263
- **Author:** @timcosta
- **Status:** CLOSED (completed)
- **Created:** 2023-06-02T17:55:49Z
- **Closed:** 2023-09-19T14:26:31Z
- **Labels:** vrl:stdlib

## Description

Hi all! I've been parsing some VPC Flow Logs with VRL, and noticed that a chunk of them are being sidelined due to errors. All of the sidelined logs have `unknown` as the value for the `account-id` column, which is [listed as possible in the AWS docs](https://docs.aws.amazon.com/vpc/latest/userguide/flow-logs.html#flow-logs-default).

VRL [appears to type account-id as an int64](https://github.com/vectordotdev/vrl/blob/2bbe6728fc0a9d0c20b6ee8634346bdbf28f78d8/src/stdlib/parse_aws_vpc_flow_log.rs#L194), which makes it fail to parse any VPC Flow logs where the account id is unknown. I believe parsing as int64 will also drop any leading `0` characters, which would make the output incorrect for any account id that has one or more leading zeroes.

Sample log with ENI and IPs obfuscated:
```
2 unknown eni-070b1422222222222 192.168.1.1 10.0.0.2 55828 60002 6 1 44 1685727399 1685727446 ACCEPT OK
```

Let me know if you need any additional information!
