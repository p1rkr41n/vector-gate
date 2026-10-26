# Issue #1063: `parse_groks` fails to parse grok

- **URL:** https://github.com/vectordotdev/vrl/issues/1063
- **Author:** @p3nal
- **Status:** CLOSED (not_planned)
- **Created:** 2024-10-04T17:47:32Z
- **Closed:** 2024-10-04T19:04:45Z
- **Labels:** None

## Description

When using `parse_groks` to parse a PAM session line from linux auth logs, it fails to parse with the exact same grok used in `parse_grok`. Now I know that these functions use different implementations of grok, but I see that the implementation used by `parse_grok` is what gets the job done in this case as tested on grokdebugger [here](https://grokdebugger.com?pattern=(%3F%3D%25%7BGREEDYDATA%3Amessage%7D)%25%7BWORD%3Apam_module%7D%5C(%25%7BDATA%3Apam_caller%7D%5C)%3A%20session%20%25%7BWORD%3Apam_session_state%7D%20for%20user%20%25%7BUSERNAME%3Ausername%7D(%3F%3A%20by%20%25%7BGREEDYDATA%3Apam_by%7D)%3F&sample=pam_unix(cron%3Asession)%3A%20session%20opened%20for%20user%20root(uid%3D0)%20by%20(uid%3D0))


- line to parse: `pam_unix(cron:session): session opened for user root(uid=0) by (uid=0)`
- Parsing using `parse_grok`:
  - VRL code:
  `. = parse_groks!(.message,
                patterns: [ "(?=%{GREEDYDATA:message})%{WORD:pam_module}\\(%{DATA:pam_caller}\\): session %{WORD:pam_session_state} for user %{USERNAME:username}(?: by %{GREEDYDATA:pam_by})?"],
                )`
  - Result:
  ![image](https://github.com/user-attachments/assets/5860a38b-1203-4b0e-8dec-c7107119aace)


- Parsing using `parse_grok`:
    - VRL code:
  `. = parse_grok!(.message,
      "(?=%{GREEDYDATA:message})%{WORD:pam_module}\\(%{DATA:pam_caller}\\): session %{WORD:pam_session_state} for user %{USERNAME:username}(?: by %{GREEDYDATA:pam_by})?"
              )`
    - Result:
    ![image](https://github.com/user-attachments/assets/96d808b5-6ed3-46ea-82fe-4268fe37f38b)
