# Issue #765: How to parse buffered messages?

- **URL:** https://github.com/vectordotdev/vrl/issues/765
- **Author:** @kodi
- **Status:** CLOSED (completed)
- **Created:** 2024-03-26T16:19:05Z
- **Closed:** 2024-03-26T16:26:18Z
- **Labels:** None

## Description

Hello, 


I am parsing syslog messages, parsing them to OTEL format, and then posting to OTEL http endpoint, and this works.
But, the caveat is that I had to set buffer size to 1, which is less than ideal.

This is my config file

```toml
 [sources.my_syslog_source]
   type = "file"
   include = ["/var/log/syslog"] # Replace with the path to your syslog file
   ignore_older = 120 # Optional: Ignore files older than 2 minutes

 [transforms.my_log_transformer]
   type = "remap"
   inputs = ["my_syslog_source"]
   ## format for OTEL logs
   source = '''
stuctured =   parse_syslog!(.message)
messageJson = parse_json!(stuctured.message)

.resourceLogs = [
    {
        "resource": {
            "attributes": [{
                "key":"service.name",
                "value" : {
                    "stringValue": stuctured.appname
                }
            }]
        },
        "scopeLogs":[{
             "scope": {},
              "logRecords": [{
                 "timeUnixNano": messageJson.timestamp,
                 "severityText": messageJson.level,
                 "body": {
                    "stringValue": messageJson.message
                 },
                 "attributes": [],
                 "traceId": messageJson.trace_id,
                 "spanId": messageJson.span_id
              }]
        }]
        
    }
] 

del(.message)
del(.file)
del(.host)
del(.source_type)
del(.timestamp)
'''

 [sinks.my_otel_sink]
   type = "http"
   inputs = ["my_log_transformer"]
   uri = "https://collector.app/v1/logs" # Replace with your OTel endpoint
   auth.strategy="basic"
   auth.user = "ds"
   auth.password = "user"
   encoding.codec = "json"
   framing.method = "newline_delimited"

[sinks.my_otel_sink.batch]
    max_events = 1
[sinks.my_otel_sink.buffer]
    type="disk"
    max_size= 1073741824 # 1GiB.
    when_full="drop_newest"

[sinks.my_otel_sink.request]
   method = "post"
   compression="gzip"
   headers."Content-Type" = "application/json"

[sinks.my_console_sink]
type = "console"
inputs = ["my_log_transformer"]
encoding.codec = "json"  
```

So this works, but he problem is, that wen buffer has more than one message, it does http POST like this:

```json
{"resourceLogs": [....]}
{"resourceLogs": [....]}
{"resourceLogs": [....]}
```

which is invalid format for OTEL http endpoint, it actually expects that all of the messages  (if more than one) go to **inside** of `resourceLogs` / `scopeLogs` array.

Since I have no idea how big the buffer is, or how to do this, I had to force sink buffer size to 1. This if for local development, and in production it will go trough a different route, but still I might need this so for some different vector -> http operations.

Is this supported, or is there a better way to achieve this?

