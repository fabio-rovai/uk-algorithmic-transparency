#!/usr/bin/env python3
"""Harvest the UK Algorithmic Transparency Recording Standard (ATRS) records.

The ATRS is the UK government standard under which public-sector bodies publish
how they use algorithmic and AI tools in decisions affecting the public. Records
are published on GOV.UK. This harvests the full set via the GOV.UK Search API and
structures each: publishing body, tool name, description and date.

GOV.UK content is Crown copyright, reused under the Open Government Licence v3.0.
"""
import json, time, urllib.parse, urllib.request
from pathlib import Path

ROOT = Path(__file__).resolve().parent.parent
OUT = ROOT / "data" / "atrs_records.json"
CSV = ROOT / "data" / "atrs_records.csv"
UA = "uk-atrs-corpus/0.1 (open research; fabio@thetesseractacademy.com)"


def get(params):
    url = "https://www.gov.uk/api/search.json?" + urllib.parse.urlencode(params, doseq=True)
    req = urllib.request.Request(url, headers={"User-Agent": UA})
    with urllib.request.urlopen(req, timeout=45) as r:
        return json.load(r)


def parse_title(title):
    # ATRS titles are usually "Publishing Body: Tool Name"
    if ":" in title:
        body, tool = title.split(":", 1)
        return body.strip(), tool.strip()
    return None, title.strip()


rows, start = [], 0
while True:
    d = get({"filter_content_store_document_type": "algorithmic_transparency_record",
             "count": 100, "start": start,
             "fields": ["title", "link", "description", "public_timestamp", "organisations"]})
    for r in d["results"]:
        body, tool = parse_title(r.get("title", ""))
        rows.append({
            "publishing_body": body,
            "tool_name": tool,
            "title": r.get("title"),
            "url": "https://www.gov.uk" + r["link"],
            "published": r.get("public_timestamp"),
            "description": r.get("description"),
            "listed_organisations": [o.get("title") for o in r.get("organisations", []) if o.get("title")],
        })
    start += 100
    if start >= d["total"]:
        break
    time.sleep(0.3)

OUT.write_text(json.dumps({"meta": {
    "source": "GOV.UK Algorithmic Transparency Recording Standard records",
    "source_url": "https://www.gov.uk/government/collections/algorithmic-transparency-recording-standard-hub",
    "licence": "Open Government Licence v3.0",
    "n_records": len(rows),
}, "records": rows}, indent=2))

import csv
with CSV.open("w", newline="") as f:
    w = csv.writer(f)
    w.writerow(["publishing_body", "tool_name", "published", "url"])
    for r in rows:
        w.writerow([r["publishing_body"], r["tool_name"], r.get("published", ""), r["url"]])

from collections import Counter
bodies = Counter(r["publishing_body"] for r in rows if r["publishing_body"])
print(f"{len(rows)} ATRS records, {len(bodies)} distinct publishing bodies")
for b, n in bodies.most_common(6):
    print(f"  {b}: {n}")
