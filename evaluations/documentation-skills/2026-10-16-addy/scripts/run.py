import json,subprocess,pathlib,concurrent.futures,time,hashlib
import argparse
parser=argparse.ArgumentParser()
parser.add_argument('--output',required=True,help='New empty directory outside the repository')
parser.add_argument('--skill',required=True,help='Pinned upstream SKILL.md')
args=parser.parse_args()
source=pathlib.Path(__file__).resolve().parent.parent
base=pathlib.Path(args.output).resolve()
if base.exists() and any(base.iterdir()): raise SystemExit('Output directory must be empty')
base.mkdir(parents=True,exist_ok=True)
cases=json.loads((source/'cases.json').read_text())
skill_path=pathlib.Path(args.skill)
expected=json.loads((source/'source.json').read_text())['sha256']
if hashlib.sha256(skill_path.read_bytes()).hexdigest()!=expected: raise SystemExit('Skill hash mismatch')
skill=skill_path.read_text()

def run(job):
 case,group,repeat=job; name=f'{case["id"]}-{group}-{repeat}';d=base/name;d.mkdir(exist_ok=True)
 prefix='这是封闭输入的文档维护测试。只根据下方材料作答，不调用工具、不读取外部文件。输出文档修改提案，不实际写入文件。不要生成子 agent。\n'
 if group=='addy':prefix+='请应用以下 Skill：\n'+skill+'\n'
 prompt=prefix+json.dumps({'request':case['request'],'files':case['files']},ensure_ascii=False)
 results=[]
 for phase in range(2 if 'followup' in case else 1):
  if phase:prompt+='\n上一轮你的回答：\n'+results[-1]['answer']+'\n现在的新输入：\n'+json.dumps(case['followup'],ensure_ascii=False)
  (d/f'prompt-{phase}.txt').write_text(prompt)
  cmd=['codex','exec','--ignore-user-config','--ephemeral','--skip-git-repo-check','-C',str(d),'-s','read-only','-m','gpt-6.1-sol','-c','model_reasoning_effort="medium"','--json','-o',str(d/f'answer-{phase}.md'),'-']
  start=time.time()
  with (d/f'events-{phase}.jsonl').open('w') as out,(d/f'stderr-{phase}.txt').open('w') as err:
   try:r=subprocess.run(cmd,input=prompt,text=True,stdout=out,stderr=err,timeout=240);code=r.returncode
   except subprocess.TimeoutExpired:code=124
  answer=(d/f'answer-{phase}.md').read_text() if (d/f'answer-{phase}.md').exists() else ''
  results.append({'phase':phase,'exit_code':code,'seconds':round(time.time()-start,1),'answer':answer})
  if code:break
 data={'name':name,'group':group,'case':case['id'],'repeat':repeat,'results':results};(d/'result.json').write_text(json.dumps(data,ensure_ascii=False,indent=2));print(name,[(r['exit_code'],len(r['answer'])) for r in results],flush=True);return data
jobs=[(c,g,r) for c in cases for g in ['baseline','addy'] for r in [1,2]]
with concurrent.futures.ThreadPoolExecutor(max_workers=3) as ex:data=list(ex.map(run,jobs))
(base/'results.json').write_text(json.dumps(data,ensure_ascii=False,indent=2))
