# Issue #533: Error since the switch to daylight saving time.

- **URL:** https://github.com/vectordotdev/vrl/issues/533
- **Author:** @MohamedEHJ
- **Status:** CLOSED (completed)
- **Created:** 2023-10-30T12:40:48Z
- **Closed:** 2023-10-30T14:37:04Z
- **Labels:** None

## Description

Hi,
I got the "input is not enough for unique date and time" when i want to parse a custom timestamp:
```console
-> vector vrl --timezone Europe/Paris 'parse_timestamp!("20231029025935", format: "%Y%m%d%H%M%S")'
function call error for "parse_timestamp" at (0:58): Invalid timestamp "20231029025935": input is not enough for unique date and time
```

I think it's related to the timezone defined, but i dont understand the behavior

Thanks! 

cf discord issue: https://discord.com/channels/742820443487993987/1168498617842159626
