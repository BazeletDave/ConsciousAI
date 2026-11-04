#!/usr/bin/env python3
"""Offline fail-closed validation of a WDI evidence archive. No external API access."""
import csv, hashlib, io, json, sys, zipfile
from collections import Counter

COUNTRIES = {"GHA","KEN","NGA","RWA","ZAF"}
INDICATORS = {"EG.ELC.ACCS.ZS","IT.NET.USER.ZS","NY.GDP.PCAP.CD","SP.POP.TOTL"}
YEARS = range(2020,2025)

def verify(path):
    with zipfile.ZipFile(path) as z:
        names=z.namelist()
        assert len(names)==len(set(names)), "duplicate archive names"
        assert all(not n.startswith("/") and ".." not in n.split("/") for n in names), "unsafe path"
        m=json.loads(z.read("evidence_manifest.json"))
        assert m["status"]=="pass" and set(m["countries"])==COUNTRIES
        assert set(m["indicators"])==INDICATORS and m["years"]==[2020,2024]
        sources={s["file"]:s for s in m["sources"]}
        expected_files={f"raw/bulk_{i}.json" for i in INDICATORS}
        expected_files|={f"raw/single_{c}_{i}.json" for c in COUNTRIES for i in INDICATORS}
        assert len(m["sources"])==len(sources)==24 and set(sources)==expected_files
        for filename,s in sources.items():
            data=z.read(filename)
            assert len(data)==s["bytes"] and hashlib.sha256(data).hexdigest()==s["sha256"],filename
        rows=list(csv.DictReader(io.StringIO(z.read("wdi_baseline.csv").decode())))
        expected=Counter((c,i,y) for c in COUNTRIES for i in INDICATORS for y in YEARS)
        actual=Counter((r["iso3"],r["indicator_code"],int(r["year"])) for r in rows)
        assert len(rows)==m["records"]==100 and actual==expected
        assert sum(r["value_status"]=="missing" for r in rows)==m["missing_records"]
        assert m["discrepancy_count"]==0 and json.loads(z.read("discrepancies.json"))==[]
        bulk={}
        for indicator in INDICATORS:
            payload=json.loads(z.read(f"raw/bulk_{indicator}.json"))
            assert len(payload)==2 and payload[0]["pages"]==1
            for item in payload[1]:
                key=(item["countryiso3code"],indicator,int(item["date"]))
                assert item["indicator"]["id"]==indicator and key in expected and key not in bulk
                bulk[key]=item["value"]
        assert set(bulk)==set(expected)
        for country in COUNTRIES:
            for indicator in INDICATORS:
                payload=json.loads(z.read(f"raw/single_{country}_{indicator}.json"))
                seen=set()
                for item in payload[1]:
                    key=(country,indicator,int(item["date"]))
                    assert item["countryiso3code"]==country and item["indicator"]["id"]==indicator
                    assert key in expected and key not in seen and item["value"]==bulk[key]
                    seen.add(key)
                assert seen=={(country,indicator,y) for y in YEARS}
        for row in rows:
            key=(row["iso3"],row["indicator_code"],int(row["year"]))
            value=bulk[key]
            assert row["value"]==("" if value is None else str(value)),key
            assert row["value_status"]==("missing" if value is None else "reported")
            assert row["response_sha256"]==sources[f"raw/bulk_{row['indicator_code']}.json"]["sha256"]
            assert row["retrieved_at_utc"]==m["retrieved_at_utc"]
        return {"status":"pass","records":len(rows),"raw_responses":len(sources),"discrepancies":0,
                "scope":"archive integrity and same-source API consistency; not independent release validation"}

if __name__=="__main__":
    if len(sys.argv)!=2: raise SystemExit("Usage: python verify_wdi_archive.py archive.zip")
    try: print(json.dumps(verify(sys.argv[1]),indent=2))
    except (AssertionError,KeyError,ValueError,zipfile.BadZipFile) as exc:
        print(f"FAIL: {exc}",file=sys.stderr)
        raise SystemExit(1)
