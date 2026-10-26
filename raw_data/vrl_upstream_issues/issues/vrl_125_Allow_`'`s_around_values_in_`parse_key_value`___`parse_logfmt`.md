# [#125] Allow `'`s around values in `parse_key_value` / `parse_logfmt`

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/125)
- **Status**: `OPEN`
- **Author**: [@jszwedko](https://github.com/jszwedko)
- **Created At**: `2021-04-15T15:48:17Z`
- **Updated At**: `2026-06-16T13:11:35Z`
- **Comments**: 0
- **Labels**: `type:enhancement`, `vrl:stdlib`, `stdlib:parse_key_value`, `stdlib:parse_logfmt`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/125)

---

## Description

Reported by user in discord: https://discord.com/channels/742820443487993987/746070591097798688/832270139293433867

They'd like to parse a line that seems to be logfmt, but with `'`s around the value instead of `"`s:

```
{"appname":"haproxy","file":"/var/log/haproxy-http.log","host":"lb1","hostname":"lb1","message":"client_ip=10.10.0.99 client_port=51428 frontend_transport=stats backend_name=stats backend_server=<PROMEX> time_to_recieve=0 slot_wait_time=0 tcp_establish_time=0 responce_time=0 request_active_time=0 status_code=200 bytes_read=45096 request_cookie=- responce_cookie=- termination_state_cookie=LR-- process_concurrent_connections=1 frontend_concurrent_connections=1 backend_concurrent_connections=0 server_concurrent_connections=0 retries_count=0 server_queue=0 backend_queue=0 request_headers= responce_headers= request='"GET /metrics HTTP/1.1"'","procid":11296,"source_type":"file","timestamp":"2021-04-15T15:02:23Z"}
```

Note the `request` key's value. It seems to be double quoted, but I think it'd be reasonable to expand `parse_key_value` and `parse_logfmt` to allow this as a delimiter as well.
