# Issue #643: parse_nginx_log fails on empty referer

- **URL:** https://github.com/vectordotdev/vrl/issues/643
- **Author:** @mtekel
- **Status:** CLOSED (completed)
- **Created:** 2024-01-16T13:30:22Z
- **Closed:** 2024-03-12T21:31:14Z
- **Labels:** None

## Description

Hello,

it seems pattern definition for nginx common log used by parse_nginx_log function expects non-empty referer: https://github.com/vectordotdev/vrl/blob/2b39353b3236e0aac26314ad47153238c52aa2ff/src/stdlib/log_util.rs#L136C1-L136C106

As it turns out, in practice, referer can be empty, see https://stackoverflow.com/questions/6880659/in-what-cases-will-http-referer-be-empty. E.g. when the enduser
> entered the site URL in browser address bar itself.
    visited the site by a browser-maintained bookmark.
    visited the site as first page in a new window/tab/session, in some browsers.
    clicked a link on a page having restrictive [<meta name="referrer">](http://wiki.whatwg.org/wiki/Meta_referrer) tag.
    clicked a link on a page having restrictive [Referrer-Policy](https://www.w3.org/TR/referrer-policy/) header.
    clicked a link having [rel="noreferrer"](https://developer.mozilla.org/en-US/docs/Web/HTML/Attributes/rel/noreferrer).
    clicked a link in an external application (i.e. not a webbrowser, e.g. Flash).
    switched from a https URL to a http URL.
    has security software installed (antivirus/firewall/etc) which strips the referrer from all requests.
    is behind a proxy which strips the referrer from all requests.
    visited the site programmatically (like, curl) without setting the referrer header (bots!).

This means that any time we get client request with empty referer, vector fails to parse nginx log line. We do get thousands of these issues each day.

Example code for vrl playground (vrl 0.9.1, vector cebe6284).

Working:
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoic3RydWN0dXJlZCA9IHBhcnNlX25naW54X2xvZyEoLm1lc3NhZ2UsXCJpbmdyZXNzX3Vwc3RyZWFtaW5mb1wiKVxuLiA9IG1lcmdlKC4sIHN0cnVjdHVyZWQpXG4iLCJldmVudCI6eyJtZXNzYWdlIjoiLSAtIC0gWzAzL09jdC8yMDIzOjE0OjIxOjM2ICswMDAwXSBcIlBPU1QgLyBIVFRQLzEuMVwiIDQ5OSAwIFwiLVwiIFwiLVwiIDExMjggMC4wMDMgW3NvbWUuYWRkcmVzcy5jb21dIFstXSBodHRwcyAwIDAuMDA0IDAwNSAxMC41My4xMzQuNDcifSwiaXNfanNvbmwiOmZhbHNlLCJlcnJvciI6bnVsbH0%3D

Broken: 
https://playground.vrl.dev/?state=eyJwcm9ncmFtIjoic3RydWN0dXJlZCA9IHBhcnNlX25naW54X2xvZyEoLm1lc3NhZ2UsXCJpbmdyZXNzX3Vwc3RyZWFtaW5mb1wiKVxuLiA9IG1lcmdlKC4sIHN0cnVjdHVyZWQpXG4iLCJldmVudCI6eyJtZXNzYWdlIjoiLSAtIC0gWzAzL09jdC8yMDIzOjE0OjIxOjM2ICswMDAwXSBcIlBPU1QgLyBIVFRQLzEuMVwiIDQ5OSAwIFwiXCIgXCItXCIgMTEyOCAwLjAwMyBbc29tZS5hZGRyZXNzLmNvbV0gWy1dIGh0dHBzIDAgMC4wMDQgMDA1IDEwLjUzLjEzNC40NyJ9LCJpc19qc29ubCI6ZmFsc2UsImVycm9yIjpudWxsfQ%3D%3D

