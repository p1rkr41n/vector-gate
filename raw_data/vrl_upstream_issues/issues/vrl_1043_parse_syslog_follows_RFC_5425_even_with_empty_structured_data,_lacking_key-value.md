# [#1043] parse_syslog follows RFC 5425 even with empty structured data, lacking key-value pairs.

- **Repository**: [vectordotdev/vrl](https://github.com/vectordotdev/vrl/issues/1043)
- **Status**: `OPEN`
- **Author**: [@itkovian](https://github.com/itkovian)
- **Created At**: `2024-09-19T18:24:12Z`
- **Updated At**: `2026-06-16T13:09:53Z`
- **Comments**: 6
- **Labels**: `vrl:stdlib`, `stdlib:parse_syslog`
- **GitHub Link**: [View on GitHub](https://github.com/vectordotdev/vrl/issues/1043)

---

## Description

We're getting a bit of junk when processing syslog lines from several applications that implement the old syslog format (RFC 3164) but are actually putting something in `[]` without key-value pairs.

I see in the tests that

~~~~
        empty_sd_element {
            args: func_args![value: r#"<13>1 2019-02-13T19:48:34+00:00 74794bfb6795 root 8449 - [empty] qwerty"#],
            want: Ok(btreemap!{
                "message" => "qwerty",
                "appname" => "root",
                "facility" => "user",
                "hostname" => "74794bfb6795",
                "message" => "qwerty",
                "procid" => 8449,
                "severity" => "notice",
                "timestamp" => chrono::Utc.ymd(2019, 2, 13).and_hms_milli(19, 48, 34, 0),
                "version" => 1,
                "empty" => btreemap! {},
            }),
            tdef: TypeDef::object(inner_kind()).fallible(),
        }
~~~~

I am wondering if this is actually the expected behaviour. What would be the rationale behind having empty structured data? Is it not more logical that these kinds of messages actually follow RFC 3164 instead of RFC 5424?

An empty structured message with information that varies wildly (e.g., a job ID (from slurm), some GC time (from Kafka)) means that the data that is shipped off to e.g. Elasticsearch will pollute the fields, as the object key may be interpreted as a fieldname with dynamic mapping turned on. 

Is there a way to control this behaviour?


