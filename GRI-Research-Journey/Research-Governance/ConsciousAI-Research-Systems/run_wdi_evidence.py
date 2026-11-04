#!/usr/bin/env python3
"""Reproducible, read-only World Bank WDI evidence capture; no model estimation."""
import csv, datetime as dt, hashlib, json, pathlib, urllib.request, urllib.parse, sys
import world_bank_africa_baseline as baseline

OUT = pathlib.Path(sys.argv[1] if len(sys.argv)>1 else 'wdi_evidence')
OUT.mkdir(parents=True, exist_ok=True)
RAW = OUT/'raw'; RAW.mkdir(exist_ok=True)
STAMP = dt.datetime.now(dt.timezone.utc).isoformat()
YEARS = (2020, 2024)
COUNTRIES = baseline.COUNTRIES
INDICATORS = baseline.INDICATORS
manifest = {'retrieved_at_utc': STAMP, 'years': list(YEARS), 'countries': list(COUNTRIES),
            'indicators': list(INDICATORS), 'sources': [], 'comparison': 'independent per-country WDI API requests; not independent publication/release'}

def fetch(url, filename):
    req=urllib.request.Request(url,headers={'User-Agent':'GRI-WDI-Evidence/1.0'})
    with urllib.request.urlopen(req,timeout=45) as response:
        status=response.status
        raw=response.read(5_000_001)
    if status != 200 or len(raw)>5_000_000: raise ValueError('HTTP status or response size invalid')
    parsed=json.loads(raw)
    if not isinstance(parsed,list) or len(parsed)<2 or not isinstance(parsed[1],list) or int(parsed[0].get('pages',1))!=1:
        raise ValueError('Invalid API payload or pagination')
    (RAW/filename).write_bytes(raw)
    manifest['sources'].append({'url':url,'file':str(pathlib.Path('raw')/filename),'sha256':hashlib.sha256(raw).hexdigest(),'bytes':len(raw),'retrieved_at_utc':dt.datetime.now(dt.timezone.utc).isoformat()})
    return parsed[1]

rows=[]; discrepancies=[]
try:
    for indicator,(label,unit) in INDICATORS.items():
        params=urllib.parse.urlencode({'format':'json','date':'2020:2024','per_page':'1000','source':'2'})
        bulk_url=f'https://api.worldbank.org/v2/country/{";".join(COUNTRIES)}/indicator/{indicator}?{params}'
        bulk=fetch(bulk_url,f'bulk_{indicator}.json')
        bulk_sha=manifest['sources'][-1]['sha256']
        lookup={}
        for r in bulk:
            key=(r.get('countryiso3code'),str(r.get('date')))
            if key in lookup: raise ValueError(f'Duplicate bulk key {indicator} {key}')
            if r.get('indicator',{}).get('id')!=indicator or key[0] not in COUNTRIES or key[1] not in [str(y) for y in range(2020,2025)]:
                raise ValueError(f'Unexpected bulk identity {indicator} {key}')
            lookup[key]=r.get('value')
        for country,name in COUNTRIES.items():
            single_url=f'https://api.worldbank.org/v2/country/{country}/indicator/{indicator}?{params}'
            single=fetch(single_url,f'single_{country}_{indicator}.json')
            per_country={}
            for r in single:
                key=(r.get('countryiso3code'),str(r.get('date')))
                if key in per_country: raise ValueError(f'Duplicate individual key {indicator} {key}')
                if r.get('indicator',{}).get('id')!=indicator or key[0]!=country or key[1] not in [str(y) for y in range(2020,2025)]:
                    raise ValueError(f'Unexpected individual identity {indicator} {key}')
                per_country[key]=r.get('value')
            for year in range(2020,2025):
                key=(country,str(year)); a=lookup.get(key); b=per_country.get(key)
                if a!=b:
                    discrepancies.append({'country':country,'indicator':indicator,'year':year,'bulk_value':a,'single_value':b})
                rows.append({'iso3':country,'country':name,'indicator_code':indicator,'indicator_label':label,'year':year,
                             'value':'' if a is None else a,'unit':unit,'value_status':'missing' if a is None else 'reported',
                             'source_url':bulk_url,'retrieved_at_utc':STAMP,
                             'response_sha256':bulk_sha})
    with (OUT/'wdi_baseline.csv').open('w',newline='',encoding='utf-8') as f:
        w=csv.DictWriter(f,fieldnames=baseline.FIELDS);w.writeheader();w.writerows(rows)
    with (OUT/'discrepancies.json').open('w',encoding='utf-8') as f: json.dump(discrepancies,f,indent=2)
    manifest['records']=len(rows)
    manifest['missing_records']=sum(r['value_status']=='missing' for r in rows)
    manifest['discrepancy_count']=len(discrepancies)
    manifest['status']='pass' if len(rows)==100 and not discrepancies else 'fail'
finally:
    (OUT/'evidence_manifest.json').write_text(json.dumps(manifest,indent=2)+'\n',encoding='utf-8')
if manifest['status']!='pass': raise SystemExit('Evidence reconciliation failed; inspect discrepancies')
print(f"PASS: {len(rows)} observations; {manifest['missing_records']} missing; {len(discrepancies)} discrepancies; {len(manifest['sources'])} raw API responses")
