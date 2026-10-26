# Issue #395: Similar to the parsing function of the Dissect filter plugin in Logstash.

- **URL:** https://github.com/vectordotdev/vrl/issues/395
- **Author:** @41405465
- **Status:** CLOSED (completed)
- **Created:** 2023-08-18T01:25:03Z
- **Closed:** 2023-08-23T15:41:36Z
- **Labels:** vrl:stdlib

## Description

Our applications log in the following format:
[20230813_060934_933][W][TcpClient.cpp::Reconnect:861]Reconnect(id:687 ip:172.26.165.6 port:20882) failed(-17)[TID:118242]

The logstash dissect parsing is implemented as follows：
dissect {
		mapping => {
			"message" => "[%{time}][%{level}][%{file}::%{function}:%{line}]%{content}[TID:%{tid}]"
		}
	}

Does Vector have a parsing function similar to the Logstash Dissect filter plugin's parsing capability?
Dissect differs from Grok in that it does not use regular expressions and is faster. Dissect works well when data is reliably repeated.
