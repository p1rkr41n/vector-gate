# Issue #1452: Feature Request: Recursive Function Support in Remap for OTLP Attribute Transformation

- **URL:** https://github.com/vectordotdev/vrl/issues/1452
- **Author:** @lsj4401
- **Status:** CLOSED (completed)
- **Created:** 2025-07-18T06:31:31Z
- **Closed:** 2025-07-22T04:34:04Z
- **Labels:** vrl:stdlib

## Description

The structure of attributes within OTLP (OpenTelemetry Protocol) can be complex, as seen in examples like this: https://github.com/open-telemetry/opentelemetry-proto/blob/main/examples/logs.json#L23.

We are currently using Vector to transform OTLP data into a flattened JSON format for ingestion into ClickHouse. To achieve this flattened JSON, recursive function calls are necessary to navigate and process the nested OTLP attribute structure.

However, Vector's remap transform currently lacks the ability to declare functions, which prevents us from implementing the required recursion directly within remap configuration. As a workaround, we are forced to use Lua for this specific transformation.

Would it be possible to add support for function declaration (and thus recursive function calls) within the remap transform? This feature would significantly simplify our configuration and reduce the need for external scripting languages like Lua for common data transformation tasks involving complex nested structures.
