"""Fetch official Statuspage JSON for each service and save data/status.json. Run by GitHub Actions every 15 minutes."""
import json,urllib.request,datetime,re,os
src=open(os.path.join(os.path.dirname(__file__),'..','gen.py')).read()
S=re.findall(r'\("([a-z0-9-]+)","[^"]+","[a-z]+","#[0-9a-f]+","(https://[^"]+)"\)',src)
out={"generated_at":datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds"),"services":{}}
for slug,base in S:
    e={"source":base+"/api/v2/status.json"}
    try:
        with urllib.request.urlopen(urllib.request.Request(e["source"],headers={"User-Agent":"DownFixer status snapshot"}),timeout=20) as r:
            d=json.load(r); e["data"]={"page":{"name":d["page"]["name"],"updated_at":d["page"]["updated_at"]},"status":d["status"]}
    except Exception as x: e["error"]=str(x)[:200]
    e["fetched_at"]=datetime.datetime.now(datetime.timezone.utc).isoformat(timespec="seconds")
    out["services"][slug]=e
os.makedirs("data",exist_ok=True); json.dump(out,open("data/status.json","w"),indent=1)
print(sum(1 for v in out["services"].values() if "data" in v),"of",len(S),"ok")
