import urllib.request
import urllib.parse
import json
import time
import os

TOKEN = os.environ.get("GITHUB_TOKEN", "")
headers = {
    "Authorization": f"Bearer {TOKEN}",
    "Accept": "application/vnd.github.v3+json",
    "User-Agent": "vector-gate-auditor"
}

queries = [
    "repo:vectordotdev/vector beats is:issue",
    "repo:vectordotdev/vector lumberjack is:issue",
    "repo:vectordotdev/vector filebeat is:issue",
    "repo:vectordotdev/vector winlogbeat is:issue",
    "repo:vectordotdev/vector metricbeat is:issue",
    "repo:vectordotdev/vector beats is:pr",
    "repo:vectordotdev/vector lumberjack is:pr",
    "repo:vectordotdev/vector filebeat is:pr"
]

all_items = {}

for q in queries:
    page = 1
    while True:
        url = f"https://api.github.com/search/issues?q={urllib.parse.quote(q)}&per_page=100&page={page}"
        req = urllib.request.Request(url, headers=headers)
        try:
            with urllib.request.urlopen(req) as resp:
                data = json.loads(resp.read().decode())
                items = data.get("items", [])
                for it in items:
                    num = it["number"]
                    if num not in all_items:
                        all_items[num] = it
                total = data.get("total_count", 0)
                if len(items) < 100 or len(all_items) >= total:
                    break
                page += 1
        except Exception as e:
            print(f"Error fetching {q} page {page}: {e}")
            break
        time.sleep(0.5)

print(f"Total unique Beats/Lumberjack/Filebeat items in vectordotdev/vector: {len(all_items)}")

issues_only = [it for it in all_items.values() if "pull_request" not in it]
prs_only = [it for it in all_items.values() if "pull_request" in it]

open_issues = [i for i in issues_only if i["state"] == "open"]
closed_issues = [i for i in issues_only if i["state"] == "closed"]
open_prs = [p for p in prs_only if p["state"] == "open"]
closed_prs = [p for p in prs_only if p["state"] == "closed"]

print(f"Total Issues: {len(issues_only)} -> Open: {len(open_issues)}, Closed: {len(closed_issues)}")
print(f"Total PRs: {len(prs_only)} -> Open: {len(open_prs)}, Closed: {len(closed_prs)}")

os.makedirs("research/beats_issues", exist_ok=True)
with open("research/beats_issues/vector_upstream_beats_all.json", "w", encoding="utf-8") as fp:
    json.dump(list(all_items.values()), fp, indent=2)

with open("research/beats_issues/vector_upstream_beats_issues.json", "w", encoding="utf-8") as fp:
    json.dump(issues_only, fp, indent=2)

with open("research/beats_issues/vector_upstream_beats_prs.json", "w", encoding="utf-8") as fp:
    json.dump(prs_only, fp, indent=2)

print("Saved files to research/beats_issues/")
