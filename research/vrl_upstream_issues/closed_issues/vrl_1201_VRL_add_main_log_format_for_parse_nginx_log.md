# Issue #1201: VRL: add `main` log format for `parse_nginx_log`

- **URL:** https://github.com/vectordotdev/vrl/issues/1201
- **Author:** @virtualtam
- **Status:** CLOSED (completed)
- **Created:** 2025-01-02T18:06:03Z
- **Closed:** 2025-01-03T17:49:37Z
- **Labels:** vrl:stdlib

## Description

### Use Cases

The `parse_nginx_log` function currently supports the following formats:

- `combined`
- `error`
- `ingress_nginx`

The official Docker images for Nginx come with a default configuration file using the `main` format, defined as:

```nginx
    log_format  main  '$remote_addr - $remote_user [$time_local] "$request" '
                      '$status $body_bytes_sent "$http_referer" '
                      '"$http_user_agent" "$http_x_forwarded_for"';
```

### Reference

These configuration files are provided by the [Nginx Linux Packages](https://nginx.org/en/linux_packages.html) repositories, and the corresponding source packages are located in the [pkg-oss](https://hg.nginx.org/pkg-oss) repository:

- [alpine/alpine/nginx.conf](https://hg.nginx.org/pkg-oss/file/tip/alpine/alpine/nginx.conf)
- [debian/debian/nginx.conf](https://hg.nginx.org/pkg-oss/file/tip/debian/debian/nginx.conf)
- [rpm/SOURCES/nginx.conf](https://hg.nginx.org/pkg-oss/file/tip/rpm/SOURCES/nginx.conf)

### Related work
- #5 and #193 
