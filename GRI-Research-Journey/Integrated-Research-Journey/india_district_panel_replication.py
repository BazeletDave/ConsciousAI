"""GRI reproducible descriptive PhonePe Pulse district panel, not causal inference.
Requires Python 3 standard library and internet access to raw.githubusercontent.com.
Run: python india_district_panel_replication.py
Produces india_district_panel.csv and india_district_summary.json locally.
"""
import csv, hashlib, json, statistics, urllib.request
from collections import defaultdict
from pathlib import Path
ROOT="https://raw.githubusercontent.com/PhonePe/pulse/main/data/map/transaction/hover/country/india/state"
states=("karnataka","bihar")
panel=defaultdict(dict); provenance=[]
for state in states:
    for year in (2023,2024):
        for quarter in (1,2,3,4):
            url=f"{ROOT}/{state}/{year}/{quarter}.json"
            with urllib.request.urlopen(url,timeout=30) as response:
                raw=response.read()
            data=json.loads(raw)
            provenance.append({"state":state,"year":year,"quarter":quarter,
                               "url":url,"sha256":hashlib.sha256(raw).hexdigest()})
            for item in data["data"]["hoverDataList"]:
                key=(state,item["name"])
                slot=(year,quarter)
                if slot in panel[key]:
                    raise ValueError(f"Duplicate: {key} {slot}")
                panel[key][slot]=int(item["metric"][0]["count"])
rows=[]; summary={}
for (state,district),values in sorted(panel.items()):
    if len(values)!=8:
        continue
    for (year,quarter),count in sorted(values.items()):
        rows.append({"state":state,"district":district,"year":year,
                     "quarter":quarter,"transactions":count})
for state in states:
    keys=[k for k,v in panel.items() if k[0]==state and len(v)==8]
    y23=sum(panel[k][(2023,q)] for k in keys for q in range(1,5))
    y24=sum(panel[k][(2024,q)] for k in keys for q in range(1,5))
    growth=[100*(sum(panel[k][(2024,q)] for q in range(1,5))/
                   sum(panel[k][(2023,q)] for q in range(1,5))-1) for k in keys]
    summary[state]={"districts":len(keys),"volume2023":y23,"volume2024":y24,
                    "aggregate_growth_pct":100*(y24/y23-1),
                    "median_district_growth_pct":statistics.median(growth)}
with open("india_district_panel.csv","w",newline="") as f:
    writer=csv.DictWriter(f,fieldnames=("state","district","year","quarter","transactions"))
    writer.writeheader();writer.writerows(rows)
Path("india_district_summary.json").write_text(json.dumps(
    {"source":"PhonePe Pulse public quarterly district JSON","rows":len(rows),
     "summary":summary,"provenance":provenance,"limitations":
     "Platform aggregates only; no treatment or causal identification."},indent=2))
print(json.dumps({"rows":len(rows),"summary":summary},indent=2))
