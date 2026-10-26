# Issue #959: Unable to decode base 64 string

- **URL:** https://github.com/vectordotdev/vrl/issues/959
- **Author:** @ManuISEN
- **Status:** CLOSED (completed)
- **Created:** 2024-07-26T15:48:41Z
- **Closed:** 2024-07-26T17:42:54Z
- **Labels:** vrl:stdlib

## Description

I'm unable to use the VRL decode_base64 function with the following string

`$ decode_base64!("eyJzY2hlbWEiOiJpZ2x1OmNvbS5zbm93cGxvd2FuYWx5dGljcy5zbm93cGxvdy91bnN0cnVjdF9ldmVudC9qc29uc2NoZW1hLzEtMC0wIiwiZGF0YSI6eyJzY2hlbWEiOiJpZ2x1OmNvbS5zbm93cGxvd2FuYWx5dGljcy5zbm93cGxvdy9saW5rX2NsaWNrL2pzb25zY2hlbWEvMS0wLTEiLCJkYXRhIjp7InRhcmdldFVybCI6Imh0dHBzOi8vaWRwLWF1dGguZ2FyLmVkdWNhdGlvbi5mci9kb21haW5lR2FyP2lkRU5UPVNqQT0maWRTcmM9WVhKck9pODBPRFUyTmk5d2RERTRNREF3TVE9PSIsImVsZW1lbnRJZCI6IiIsImVsZW1lbnRDbGFzc2VzIjpbImxpbmstYnV0dG9uIiwidHJhY2tlZCJdLCJlbGVtZW50VGFyZ2V0IjoiX2JsYW5rIn19fQ")
function call error for "decode_base64" at (0:500): unable to decode value to base64
` 

I can decode it outside VRL. It seems related to the URL in it.

Here below the decoded string with Notepad++.

`{"schema":"iglu:com.snowplowanalytics.snowplow/unstruct_event/jsonschema/1-0-0","data":{"schema":"iglu:com.snowplowanalytics.snowplow/link_click/jsonschema/1-0-1","data":{"targetUrl":"https://idp-auth.gar.education.fr/domaineGar?idENT=SjA=&idSrc=YXJrOi80ODU2Ni9wdDE4MDAwMQ==","elementId":"","elementClasses":["link-button","tracked"],"elementTarget":"_blank"}}}`
