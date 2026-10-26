# Issue #246: how to effectively apply multiple parsers with parse_groks and parse_regex

- **URL:** https://github.com/vectordotdev/vrl/issues/246
- **Author:** @dss010101
- **Status:** CLOSED (not_planned)
- **Created:** 2023-05-16T22:50:09Z
- **Closed:** 2023-05-16T22:55:22Z
- **Labels:** None

## Description

Hi,
i have logs that can look like shown below.  There could be other variations.
I'd like to parse these, and in the case where there is a pattern 'app_id:<some_id>', also parse that out.
```
[2023-05-15 11:52:29,401][2555:140431094425152][INFO][app_service.run] initalizing application
[2023-05-15 11:53:29,401][2555:140431094425152][INFO][app_service.run] app_id:my_app_12345 initialized.
[2023-05-15 11:54:29,401][2555:140431094425152]INFO:app_service: request recieved with args...
```

I've tried parse_groks, with some success..but for some reason parsing the run_id does not seem to work for me:
```
source = '''
    . |= parse_groks!(
            .message, 
            patterns:[
                "\\[%{TIMESTAMP_ISO8601:log_time}\\]\\[%{INT:pid}:%{INT:tid}\\]\\[%{WORD:severity}\\]\\[%{WORD:module}.%{WORD:func}\\] %{GREEDYDATA:msg}",
                "\\[%{TIMESTAMP_ISO8601:log_time}\\]\\[%{INT:pid}:%{INT:tid}\\]\\[%{WORD:severity}\\]\\[%{WORD:module}.%{WORD:func}\\] app_id:%{NOTSPACE:app_id} %{GREEDYDATA:msg}",
                "\\[%{TIMESTAMP_ISO8601:log_time}\\]\\[%{INT:pid}:%{INT:tid}\\]%{WORD:severity}:%{WORD:module}:%{GREEDYDATA:msg}"
            ]
    )
'''
```

Also read that grok internally uses regex, so thought maybe it would be more efficient to use regex as id be removing one layer...but cant find much documentation or examples on how to do multiple parsing or 'sub-parsing' of fields.  Tried below, where the first part by itself works, but i am not then able to split the .msg field into app_id and the actual message.  that throws the exception: "this expression must resolve to an object"

```
source = '''
    . |= parse_regex!(
                .message, 
                pattern: r'^\[(?P<log_time>.+)\]\[(?P<pid>\d+):(?P<tid>\d+)\]\[(?P<severity>\w+)\]\[(?P<module>\w+)\.(?P<func>\w+)\] (?P<msg>.*$)'
        )
    .msg |= parse_regex!(
                .msg, 
                pattern: r'^.+app_id:(?P<app_id>\w+) (?P<msg>.*)$'
        )

'''
```

Any help on trying to get this right is appreciated...

