# [#946] parse_vector VRL function?

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/946)
- **Status**: `OPEN`
- **Author**: [@davidpellcb](https://github.com/davidpellcb)
- **Created At**: `2024-07-16T01:28:15Z`
- **Updated At**: `2024-07-18T21:17:25Z`
- **Comments**: 3
- **Labels**: `type:enhancement`, `vrl:stdlib`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/946)

---

## Description

I'm looking for a way to parse the logs emitted by Vector itself. AFAICT there isn't a `parse_*` function for this.

Example log:
```
2024-07-11T17:56:52.024579Z  WARN vector::kubernetes::reflector: Watcher Stream received an error. Retrying. error=InitialListFailed(Api(ErrorResponse { status: "Failure", message: "pods is forbidden: User \"system:serviceaccount:local-utility:vector-agent\" cannot list resource \"pods\" in API group \"\" at the cluster scope: RBAC: clusterrole.rbac.authorization.k8s.io \"vector-agent\" not found", reason: "Forbidden", code: 403 })
```

Is there a recommended approach for parsing Vector's logs? Just `parse_grok` or `parse_regex`? Seems like this may be hard to do. Compare this other WARN log:

```
2024-07-16T02:01:33.917564Z  WARN sink{component_kind="sink" component_id=proxy component_type=http}:request{request_id=1532040}: vector::sinks::util::retries: Retrying after response. reason=Http Status: 500 Internal Server Error internal_log_rate_limit=true
```
