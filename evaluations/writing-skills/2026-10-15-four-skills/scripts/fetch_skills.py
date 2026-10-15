"""Download skill files at immutable commits; never install them globally."""
import concurrent.futures, hashlib, json, subprocess, urllib.request
from pathlib import Path
ROOT=Path(__file__).resolve().parents[1]
SOURCES={'clear':('softaworks/agent-toolkit','skills/writing-clearly-and-concisely'),'humanizer':('blader/humanizer',''),'ste':('danyuchn/asd-ste100-skill',''),'adhd':('ayghri/i-have-adhd','skills/i-have-adhd')}
CLEAR=['SKILL.md','README.md','signs-of-ai-writing.md']+['elements-of-style/'+x+'.md' for x in ['01-introductory','02-elementary-rules-of-usage','03-elementary-principles-of-composition','04-a-few-matters-of-form','05-words-and-expressions-commonly-misused']]
def pin(item):
 name,(repo,sub)=item
 sha=subprocess.run(['git','ls-remote','https://github.com/'+repo+'.git','HEAD'],capture_output=True,text=True,check=True,timeout=45).stdout.split()[0]
 files=CLEAR if name=='clear' else [str(p.relative_to(ROOT/'snapshots'/name)) for p in (ROOT/'snapshots'/name).rglob('*') if p.is_file()]
 assert files
 return name,dict(repository=repo,commit=sha,path=sub,files={f:None for f in files})
if (ROOT/'sources.json').exists():
 result=json.loads((ROOT/'sources.json').read_text())
elif (ROOT/'protocol.json').exists():
 result=json.loads((ROOT/'protocol.json').read_text())['sources']
else:
 with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool: result=dict(pool.map(pin,SOURCES.items()))
def fetch(job):
 name,f=job;info=result[name]
 url='https://raw.githubusercontent.com/'+info['repository']+'/'+info['commit']+'/'+('/'.join(x for x in [info['path'],f] if x))
 data=urllib.request.urlopen(url,timeout=30).read()
 p=ROOT/'snapshots'/name/f;p.parent.mkdir(parents=True,exist_ok=True);p.write_bytes(data)
 return name,f,hashlib.sha256(data).hexdigest()
with concurrent.futures.ThreadPoolExecutor(max_workers=6) as pool:
 for name,f,sha in pool.map(fetch,[(n,f) for n,v in result.items() for f in v['files']]):result[name]['files'][f]=sha
(ROOT/'sources.json').write_text(json.dumps(result,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({k:{'commit':v['commit'],'files':len(v['files'])} for k,v in result.items()},indent=2))
