# Issue #861: parse_aws_alb_log fails when processing logs containing newly added fields

- **URL:** https://github.com/vectordotdev/vrl/issues/861
- **Author:** @MingoYin
- **Status:** CLOSED (completed)
- **Created:** 2024-05-29T08:00:49Z
- **Closed:** 2024-05-29T08:01:40Z
- **Labels:** None

## Description

Hi, I encountered a problem when using parse_aws_alb_log.
The aws alb access log recently added a new field that caused parse_aws_alb_log to fail when parsing the log.
Could you please arrange to fix this issue?

ALB Access Log:
h2 2024-05-28T08:12:36.431832Z app/xxxxxx-lb/xxxxxxx 10.10.10.10:13624 1.1.1.1:8000 0.000 0.177 0.000 200 200 961 2071 "GET https://xxx.xx:443/ HTTP/2.0" "Mozilla/5.0 (iPhone; CPU iPhone OS 16_7_8 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) Version/16.6 Mobile/15E148 Safari/604.1" TLS_AES_128_GCM_SHA256 TLSv1.3 arn:aws:elasticloadbalancing:ap-northeast-1:00000000000:targetgroup/xxxxxxx/fc465292d29 "Root=1-665591f4-15d57af7699b090b59a269b4" "xxxxxx.xx" "arn:aws:acm:ap-northeast-1:0000000000000:certificate/5ceabee6-9244-4331-9690-xxxxxxxxxx" 10160 2024-05-28T08:12:36.254000Z "forward" "-" "-" "172.16.140.164:8000" "200" "-" "-" TID_37acbe0641d1c34287fee137ef3a5286


vector Log:

2024-05-29T06:45:03.369921Z ERROR transform{component_kind="transform" component_id=aws_s3_elb_tf component_type=remap}: vector::internal_events::remap: Mapping failed with event. error="function call error for \"parse_aws_alb_log\" at (5:33): Log should be fully consumed: \" TID_3bef4ecd0c08524ea9791ca8d6827c46\"" error_type="conversion_failed" stage="processing" internal_log_rate_limit=true


thanks!!!!

