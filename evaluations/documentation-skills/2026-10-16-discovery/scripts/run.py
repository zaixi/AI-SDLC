import argparse, concurrent.futures, hashlib, json, pathlib, shutil, subprocess, time, threading
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True)
parser.add_argument('--skill',required=True)
parser.add_argument('--only',nargs='*',help='Run only named trajectories in a fresh output directory')
a=parser.parse_args(); source=pathlib.Path(__file__).resolve().parent.parent
base=pathlib.Path(a.output).resolve()
if base.exists() and any(base.iterdir()):raise SystemExit('Output must be new or empty')
base.mkdir(parents=True,exist_ok=True)
skill=pathlib.Path(a.skill).read_bytes()
expected=json.loads((source.parent/'2026-10-16-addy/source.json').read_text())['sha256']
if hashlib.sha256(skill).hexdigest()!=expected:raise SystemExit('Wrong skill snapshot')
cases=json.loads((source/'cases.json').read_text())
def shell(cmd,cwd):return subprocess.run(cmd,cwd=cwd,text=True,capture_output=True)
quota_stop=threading.Event()
def run(job):
 case,group,repeat=job;name=f'{case["id"]}-{group}-{repeat}'
 if quota_stop.is_set():return {'name':name,'status':'not_started_quota'}
 d=base/name;repo=d/'repo';repo.mkdir(parents=True)
 for path,content in case['files'].items():
  f=repo/path;f.parent.mkdir(parents=True,exist_ok=True);f.write_text(content)
 if group!='baseline':
  f=repo/'.agents/skills/documentation-and-adrs/SKILL.md';f.parent.mkdir(parents=True);f.write_bytes(skill)
 for cmd in [['git','init','-q'],['git','config','user.name','Evaluation'],['git','config','user.email','evaluation@example.invalid'],['git','add','.'],['git','commit','-qm','Initial fixture']]:
  r=shell(cmd,repo)
  if r.returncode:raise RuntimeError(r.stderr)
 pre=shell(['python','-m','unittest','discover','-s','tests','-v'],repo)
 (d/'before-tests.txt').write_text(pre.stdout+pre.stderr)
 if pre.returncode:raise RuntimeError('Invalid fixture')
 prompt='只在当前仓库内工作，不读取仓库外文件、不联网、不调用子 agent、不提交 Git。完成后简要说明改动和验证。\n'+case['request']
 if group=='explicit':prompt+='\n请使用 $documentation-and-adrs 完成此次任务。'
 (d/'prompt.txt').write_text(prompt)
 cmd=['codex','exec','--ignore-user-config','--ephemeral','-C',str(repo),'-s','workspace-write','-m','gpt-6.1-sol','-c','model_reasoning_effort="medium"','--json','-o',str(d/'answer.md'),'-']
 start=time.time()
 with (d/'events.jsonl').open('w') as out,(d/'stderr.txt').open('w') as err:
  try:r=subprocess.run(cmd,input=prompt,text=True,stdout=out,stderr=err,timeout=300);code=r.returncode
  except subprocess.TimeoutExpired:code=124
 if 'usage limit' in (d/'events.jsonl').read_text().lower():quota_stop.set()
 (d/'diff.patch').write_text(shell(['git','diff','HEAD'],repo).stdout)
 (d/'status.txt').write_text(shell(['git','status','--short'],repo).stdout)
 result={'name':name,'case':case['id'],'group':group,'repeat':repeat,'exit_code':code,'seconds':round(time.time()-start,1)}
 (d/'result.json').write_text(json.dumps(result,indent=2));print(json.dumps(result),flush=True);return result
jobs=[(c,g,r) for c in cases for g in ['baseline','discoverable','explicit'] for r in [1,2]]
if a.only:jobs=[j for j in jobs if f'{j[0]["id"]}-{j[1]}-{j[2]}' in a.only]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as pool:results=list(pool.map(run,jobs))
(base/'results.json').write_text(json.dumps(results,indent=2)+'\n')
