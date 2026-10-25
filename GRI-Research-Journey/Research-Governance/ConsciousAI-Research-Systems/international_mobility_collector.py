"""GRI international and mobility source discovery. RSS/Atom only, review gated.
Publisher feed URLs are candidates, not independently certified official endpoints.
"""
import argparse,hashlib,json,tempfile,os
from datetime import datetime,timezone
from pathlib import Path
from urllib.request import Request,urlopen
from urllib.parse import urlparse
from xml.etree import ElementTree as ET
ROOT=Path(__file__).resolve().parent
SOURCES=[
 {"id":"EU-COMMISSION-NEWS","category":"international_regulatory","jurisdiction":"EU","feed":"https://digital-strategy.ec.europa.eu/en/rss.xml","publisher":"European Commission Digital Strategy"},
 {"id":"UK-DfT","category":"international_regulatory","jurisdiction":"UK","feed":"https://www.gov.uk/government/organisations/department-for-transport.atom","publisher":"UK Department for Transport"},
 {"id":"NHTSA","category":"mobility_industry","jurisdiction":"US","feed":"https://www.nhtsa.gov/press-releases/rss.xml","publisher":"NHTSA"},
 {"id":"UBER-ENGINEERING","category":"mobility_industry","jurisdiction":"corporate","feed":"https://www.uber.com/blog/engineering/rss/","publisher":"Uber Engineering"},
]
# Candidate endpoints may fail or redirect; a failed source is reported, never silently marked healthy.
def parse_feed(data,source):
 root=ET.fromstring(data)
 items=[]
 for node in root.findall(".//item")+root.findall(".//{http://www.w3.org/2005/Atom}entry"):
  def get(tag):
   e=node.find(tag);return (e.text or "").strip() if e is not None else ""
  title=get("title") or get("{http://www.w3.org/2005/Atom}title")
  link=get("link")
  if not link:
   el=node.find("{http://www.w3.org/2005/Atom}link")
   link=el.get("href","") if el is not None else ""
  if not title or not link.startswith("https://"):continue
  if urlparse(link).hostname is None:continue
  digest=hashlib.sha256((source["id"]+"|"+link).encode()).hexdigest()[:20]
  items.append({"id":digest,"source_id":source["id"],"publisher":source["publisher"],
   "jurisdiction":source["jurisdiction"],"category":source["category"],"title":title[:350],
   "source_url":link,"verification_status":"publisher_feed_item_unreviewed",
   "human_review_required":True,"publication_authorized":False})
 return items
def collect(fetch=None,sources=None,now=None):
 sources=sources if sources is not None else SOURCES
 if fetch is None:
  def fetch(url):
   with urlopen(Request(url,headers={"User-Agent":"GRI-Research-Intelligence/0.2","Accept":"application/rss+xml, application/atom+xml, application/xml"}),timeout=12) as r:
    if urlparse(r.url).scheme!="https":raise ValueError("non HTTPS redirect")
    data=r.read(1000000)
    return data
 queue={};health=[]
 for src in sources:
  try:
   if urlparse(src["feed"]).scheme!="https":raise ValueError("source must use HTTPS")
   rows=parse_feed(fetch(src["feed"]),src)
   for row in rows[:30]:queue[row["id"]]=row
   health.append({"source_id":src["id"],"status":"fetched","items":len(rows)})
  except (OSError,ValueError,ET.ParseError,KeyError) as e:
   health.append({"source_id":src["id"],"status":"failed","error_type":type(e).__name__})
 return {"schema_version":"1.0","generated_at":now or datetime.now(timezone.utc).isoformat(),
  "mode":"candidate_publisher_feed_discovery","sources":health,"queue":list(queue.values())[:120],
  "review_required":len(queue),"notice":"Publisher feed metadata is unreviewed. Feed availability and publisher identity must be validated; no independent verification or trained ML classification."}
def main():
 p=argparse.ArgumentParser();p.add_argument("--output",type=Path,default=ROOT/"international_mobility_feed.json");a=p.parse_args()
 result=collect()
 with tempfile.NamedTemporaryFile("w",dir=a.output.parent,encoding="utf8",delete=False) as f:
  json.dump(result,f,indent=2);f.write("\n");name=f.name
 os.replace(name,a.output)
 print(json.dumps({"sources":result["sources"],"items":len(result["queue"])}))
if __name__=="__main__":main()
