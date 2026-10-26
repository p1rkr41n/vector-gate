import urllib.request
import urllib.parse
import json
import time

TOKEN = os.environ.get("GITHUB_TOKEN", "")
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "vector-gate-auditor"
}

search_queries = [
    'repo:vectordotdev/vector label:"source:logstash"',
    'repo:vectordotdev/vector "logstash" in:title',
    'repo:vectordotdev/vector "beats" in:title',
    'repo:vectordotdev/vector "filebeat" in:title',
    'repo:vectordotdev/vector "lumberjack" in:title',
    'repo:vectordotdev/vector "logstash source"',
    'repo:vectordotdev/vector "beats source"',
    'repo:vectordotdev/vector "filebeat" is:issue',
    'repo:vectordotdev/vector "lumberjack" is:issue',
]

all_items = {}

for q in search_queries:
    page = 1
    while True:
        url = f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&per_page=100&page={page}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                items = data.get("items", [])
                for it in items:
                    all_items[it["number"]] = it
                total = data.get("total_count", 0)
                if len(items) < 100 or len(all_items) >= total:
                    break
                page += 1
        except Exception as e:
            print(f"Error on {q}: {e}")
            break
        time.sleep(0.4)

print(f"Total raw items collected across all queries: {len(all_items)}")

# Filter genuinely relevant items (Beats / Lumberjack / Filebeat / Logstash Source)
genuine_items = {}
for num, it in all_items.items():
    title = it["title"].lower()
    body = (it.get("body") or "").lower()
    labels = [l["name"].lower() for l in it.get("labels", [])]
    
    # Must explicitly mention beats, filebeat, winlogbeat, metricbeat, lumberjack,
    # or logstash source/input/server (not just logstash transform or sink if unrelated)
    is_relevant = False
    
    if "source:logstash" in labels:
        is_relevant = True
    elif any(k in title for k in ["beat", "beats", "filebeat", "winlogbeat", "metricbeat", "lumberjack"]):
        is_relevant = True
    elif "logstash" in title and any(k in title for k in ["source", "input", "panic", "framing", "crash", "tls", "ack", "protocol", "port", "connect", "server"]):
        is_relevant = True
    elif any(k in body for k in ["sources.logstash", "source: logstash", "lumberjack", "filebeat", "elastic beats", "protocol: beats"]):
        is_relevant = True
    elif "logstash source" in body or "beats source" in body:
        is_relevant = True
        
    if is_relevant:
        genuine_items[num] = it

print(f"Total verified Beats/Lumberjack/Logstash-Source items: {len(genuine_items)}")

issues = [it for it in genuine_items.values() if "pull_request" not in it]
prs = [it for it in genuine_items.values() if "pull_request" in it]

open_issues = [i for i in issues if i["state"] == "open"]
closed_issues = [i for i in issues if i["state"] == "closed"]

open_prs = [p for p in prs if p["state"] == "open"]
closed_prs = [p for p in prs if p["state"] == "closed"]

print(f"\n--- ISSUES ({len(issues)} total) ---")
print(f"Open: {len(open_issues)} | Closed: {len(closed_issues)}")

print(f"\n--- PULL REQUESTS ({len(prs)} total) ---")
print(f"Open: {len(open_prs)} | Closed: {len(closed_prs)}")

# Output summary of issues
with open("research/beats_issues/verified_beats_issues.json", "w", encoding="utf-8") as fp:
    json.dump(issues, fp, indent=2)

with open("research/beats_issues/verified_beats_prs.json", "w", encoding="utf-8") as fp:
    json.dump(prs, fp, indent=2)
