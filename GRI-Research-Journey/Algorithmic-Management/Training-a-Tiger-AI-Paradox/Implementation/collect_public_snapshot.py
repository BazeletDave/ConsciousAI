"""Read public research endpoints and retain timestamped responses. No account access."""
from concurrent.futures import ThreadPoolExecutor
from datetime import datetime,timezone
from pathlib import Path
import urllib.request,json
BASE='https://gri-global-intelligence.onrender.com'
PATHS=['/health','/health/collections','/intelligence/summary','/assurance/overview','/governance/assurance-evidence']
def one(path):
 start=datetime.now(timezone.utc).isoformat()
 try:
  with urllib.request.urlopen(BASE+path,timeout=20) as r:
   raw=r.read(1000000);return {'url':BASE+path,'observed_at':start,'http_status':r.status,'response':json.loads(raw)}
 except Exception as e:return {'url':BASE+path,'observed_at':start,'error':str(e)}
if __name__=='__main__':
 with ThreadPoolExecutor(max_workers=5) as pool:rows=list(pool.map(one,PATHS))
 out=Path(__file__).parent/'results/public_snapshot.json';out.write_text(json.dumps({'mode':'read_only_point_in_time_observation','endpoints':rows},indent=2)+'\n')
 print(json.dumps([{'url':x['url'],'http_status':x.get('http_status'),'error':x.get('error')} for x in rows],indent=2))
