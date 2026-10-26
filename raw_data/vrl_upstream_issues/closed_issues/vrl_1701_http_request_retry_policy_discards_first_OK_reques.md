# Issue #1701: `http_request` retry policy discards first OK request

- **URL:** https://github.com/vectordotdev/vrl/issues/1701
- **Author:** @thomasqueirozb
- **Status:** CLOSED (completed)
- **Created:** 2026-03-11T18:09:25Z
- **Closed:** 2026-03-20T18:34:18Z
- **Labels:** None

## Description

### A note for the community

<!-- Please keep this note for the community -->
* Please vote on this issue by adding a 👍 [reaction](https://blog.github.com/2016-03-10-add-reactions-to-pull-requests-issues-and-comments/) to the original issue to help the community and maintainers prioritize this request
* If you are interested in working on this issue or have submitted a pull request, please leave a comment.
<!-- Thank you for keeping this note for the community -->


### Problem

Behavior observed with the following scripts

server
```py
#!/usr/bin/env python3
"""
Simple HTTP server that returns 500 N times before returning 200.

Usage: python3 flaky_server.py <fail_count> [port]
  fail_count  number of 500 responses before returning 200
  port        port to listen on (default: 8080)
"""

import sys
from http.server import BaseHTTPRequestHandler, HTTPServer

fail_count = 0
request_count = 0


class Handler(BaseHTTPRequestHandler):
    def do_GET(self):
        global request_count
        request_count += 1
        if request_count % (fail_count + 1) != 0:
            self.send_response(500)
            self.end_headers()
            self.wfile.write(f"Error (attempt {request_count}/{fail_count})\n".encode())
            print(f"Request {request_count}: 500")
        else:
            self.send_response(200)
            self.end_headers()
            self.wfile.write(b"OK\n")
            print(f"Request {request_count}: 200")

    def log_message(self, format, *args):
        pass  # suppress default access log


if __name__ == "__main__":
    if len(sys.argv) < 2:
        print(__doc__)
        sys.exit(1)

    fail_count = int(sys.argv[1])
    port = int(sys.argv[2]) if len(sys.argv) > 2 else 8080

    print(f"Listening on :{port} — will 500 for first {fail_count} request(s)")
    HTTPServer(("", port), Handler).serve_forever()
```

## Reproducer:

Start the server
```sh
./scripts/flaky_server.py 2
```

Run vrl
```sh
echo 'http_request!("http://localhost:8080/")' | cargo run -p vrl-cli -q -- -q
```

output:
```
Listening on :8080 — will 500 for first 2 request(s)
Request 1: 500
Request 2: 500
Request 3: 200
Request 4: 500
Request 5: 500
Request 6: 200
```


### VRL Program

```text

```

### VRL and/or Vector Version

main

### Debug Output

```text

```

### Example

_No response_

### Additional Context

_No response_

### References

_No response_
