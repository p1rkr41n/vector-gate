# Issue #1359: Add `http_get` function to VRL

- **URL:** https://github.com/vectordotdev/vrl/issues/1359
- **Author:** @benjamin-awd
- **Status:** CLOSED (completed)
- **Created:** 2025-03-25T12:45:41Z
- **Closed:** 2025-08-20T17:15:13Z
- **Labels:** vrl:stdlib

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->

Currently there is no built-in way to fetch external data dynamically (other than enrichment tables, which are static files). This affects use cases where logs or other kinds of data need to be enriched with real-time information from external services.

I think it would be nice to have a function that enables a dynamic lookup for data that changes frequently.

### Use Cases

**1. Checking threat intelligence feeds**
For example, logs contain `source_ip`, and we want to check if it's flagged as malicious using a threat intelligence API:
```yaml
transforms:
  check_threat:
    type: "remap"
    inputs: ["parse_logs"]
    source: |
      threat_data = http_get!("https://threat-api.com/check?ip=" + .source_ip)
      .threat_level = parse_json!(threat_data).risk_score
```

**2. Checking cloud metadata for infrastructure logs**
Logs from cloud instances include instance_id, but we want want to fetch real-time metadata from a cloud provider which can be quite dynamic (auto-scaling changes, region changes etc).
```yaml
transforms:
  fetch_instance_metadata:
    type: "remap"
    inputs: ["parse_logs"]
    source: |
      metadata = http_get!("http://metadata.google.internal/computeMetadata/v1/instance?alt=json")
      .metadata = parse_json!(metadata)
```

### Attempted Solutions

_No response_

### Proposal

I managed to hack a rough solution together, which is currently running in my dev environment:
```rust
static CLIENT: LazyLock<Client> = LazyLock::new(reqwest::Client::new);

async fn http_get(url: &Value, auth: Option<&Value>) -> Resolved {
    let url_str = url.try_bytes_utf8_lossy()?;

    let request = CLIENT.get(url_str.as_ref());

    let response = request
        .send()
        .await
        .map_err(|e| format!("HTTP request failed: {e}"))?;

    let body = response
        .text()
        .await
        .map_err(|e| format!("Failed to read response body: {e}"))?;

    Ok(body.into())
}

...

#[derive(Debug, Clone)]
struct HttpGetFn {
    url: Box<dyn Expression>
}

impl FunctionExpression for HttpGetFn {
    fn resolve(&self, ctx: &mut Context) -> Resolved {
        let url = self.url.resolve(ctx)?;

        // block_in_place runs the HTTP request synchronously
        // without blocking Tokio's async worker threads.
        // This temporarily moves execution to a blocking-compatible thread.
        tokio::task::block_in_place(|| {
            let handle = tokio::runtime::Handle::current();

            handle.block_on(async {
                http_get(&url).await
            })
        })
    }

    fn type_def(&self, _: &TypeState) -> TypeDef {
        TypeDef::bytes().fallible()
    }
}
```

This suffers from the same drawbacks as the current `dns_lookup` function where a lot of HTTP requests could lead to performance degradations in high volume pipelines. This could be mitigated with some kind of caching mechanism, but either way I think this is a useful function to have (especially for our situation where we are using the HTTP client i.e. a very low volume source).

### References

https://github.com/vectordotdev/vector/pull/20495
