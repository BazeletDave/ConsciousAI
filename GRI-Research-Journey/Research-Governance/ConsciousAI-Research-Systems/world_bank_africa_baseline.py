#!/usr/bin/env python3
"""GRI World Bank WDI Africa baseline collector. Standard library only.
Fetches live API values; does not fill missing values, train a model, or publish.
Usage: python3 world_bank_africa_baseline.py --output africa_wdi_baseline.csv
"""
import argparse, csv, datetime as dt, hashlib, json, pathlib, urllib.parse, urllib.request

COUNTRIES = {"GHA":"Ghana","KEN":"Kenya","NGA":"Nigeria","RWA":"Rwanda","ZAF":"South Africa"}
INDICATORS = {
    "EG.ELC.ACCS.ZS":("Access to electricity","percent_population"),
    "IT.NET.USER.ZS":("Individuals using the Internet","percent_population"),
    "NY.GDP.PCAP.CD":("GDP per capita","current_USD"),
    "SP.POP.TOTL":("Population, total","persons"),
}
BASE="https://api.worldbank.org/v2"
FIELDS=["iso3","country","indicator_code","indicator_label","year","value","unit","source_url","retrieved_at_utc","response_sha256","value_status"]
def collect(start_year,end_year):
    stamp=dt.datetime.now(dt.timezone.utc).isoformat()
    rows=[]
    for code,(label,unit) in INDICATORS.items():
        country_ids=";".join(COUNTRIES)
        url=f"{BASE}/country/{country_ids}/indicator/{code}?"+urllib.parse.urlencode({"format":"json","date":f"{start_year}:{end_year}","per_page":"1000","source":"2"})
        req=urllib.request.Request(url,headers={"User-Agent":"GRI-Research/1.0 (research; source-attributed)"})
        with urllib.request.urlopen(req,timeout=25) as response:
            raw=response.read(5_000_001)
            if len(raw)>5_000_000: raise ValueError("Oversized API response")
        digest=hashlib.sha256(raw).hexdigest()
        data=json.loads(raw)
        if not isinstance(data,list) or len(data)<2 or not isinstance(data[1],list): raise ValueError(f"Unexpected API response for {code}: {data}")
        if int(data[0].get("pages",1))!=1: raise ValueError("Pagination exceeded: refuse partial dataset")
        by_key={}
        for item in data[1]:
            if not isinstance(item,dict): raise ValueError("Invalid API record")
            key=(item.get("countryiso3code"),str(item.get("date")))
            if key in by_key: raise ValueError(f"Duplicate API record for {code}: {key}")
            record_indicator=item.get("indicator")
            if not isinstance(record_indicator,dict) or record_indicator.get("id")!=code:
                raise ValueError(f"Indicator identity mismatch for {code}: {key}")
            if key[0] not in COUNTRIES or not str(key[1]).isdigit() or not start_year<=int(key[1])<=end_year:
                raise ValueError(f"Unexpected country/year for {code}: {key}")
            by_key[key]=item
        for iso,name in COUNTRIES.items():
            for year in range(start_year,end_year+1):
                item=by_key.get((iso,str(year)))
                value=None if item is None else item.get("value")
                rows.append({"iso3":iso,"country":name,"indicator_code":code,"indicator_label":label,"year":year,"value":"" if value is None else value,"unit":unit,"source_url":url,"retrieved_at_utc":stamp,"response_sha256":digest,"value_status":"missing" if value is None else "reported"})
    return rows
def main():
    parser=argparse.ArgumentParser()
    parser.add_argument("--output",default="africa_wdi_baseline.csv")
    parser.add_argument("--start-year",type=int,default=2020)
    parser.add_argument("--end-year",type=int,default=2024)
    args=parser.parse_args()
    if not 1990<=args.start_year<=args.end_year<=2026: parser.error("Invalid years")
    rows=collect(args.start_year,args.end_year)
    path=pathlib.Path(args.output)
    path.parent.mkdir(parents=True,exist_ok=True)
    with path.open("w",newline="",encoding="utf-8") as fh:
        writer=csv.DictWriter(fh,fieldnames=FIELDS)
        writer.writeheader();writer.writerows(rows)
    print(f"Wrote {len(rows)} source-qualified records to {path}")
if __name__=="__main__": main()
