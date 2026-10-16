"""Recheck completed real-file trajectories without consulting model claims."""
import argparse, hashlib, json, pathlib, subprocess, re
p=argparse.ArgumentParser();p.add_argument('--original',required=True);p.add_argument('--retry',required=True);p.add_argument('--output',required=True);a=p.parse_args()
original=pathlib.Path(a.original);retry=pathlib.Path(a.retry)
selected=[original/'01-retention-change-baseline-1']+sorted(d for d in retry.iterdir() if d.is_dir() and (d/'result.json').exists())
results=[]
for d in selected:
 r=json.loads((d/'result.json').read_text());repo=d/'repo'
 events=[json.loads(line) for line in (d/'events.jsonl').read_text().splitlines() if line.strip()]
 r['completed']=any(e.get('type')=='turn.completed' for e in events)
 r['raw_directory']=str(d)
 r['events_sha256']=hashlib.sha256((d/'events.jsonl').read_bytes()).hexdigest()
 commands=[e['item'] for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='command_execution']
 r['skill_read_commands']=[c.get('command') for c in commands if re.search(r'\bcat\s+[^;]*\.agents/skills/documentation-and-adrs/SKILL\.md',c.get('command','')) and c.get('exit_code')==0]
 r['commands_count']=len(commands)
 if r['completed']:
  checks='from service import download,total_amount,ARTIFACT_TTL,AUDIT_TTL\nassert AUDIT_TTL==2592000\nassert total_amount([])==0\nassert total_amount([7,-2,10])==15\n'
  if r['case']=='01-retention-change':
   checks+='assert ARTIFACT_TTL==86400\nfor age,want in [(86399,(200,"url")),(86400,(410,None)),(86401,(410,None))]:\n assert download(100,100+age,"url")==want\n'
  else:
   checks+='assert ARTIFACT_TTL==604800\nassert download(0,604800,"url")== (200,"url")\nassert download(0,604801,"url")== (410,None)\n'
  for label,cmd in [('test_suite',['python','-m','unittest','discover','-s','tests','-v']),('independent_checks',['python','-c',checks])]:
   out=subprocess.run(cmd,cwd=repo,text=True,capture_output=True,timeout=30)
   r[label+'_passed']=out.returncode==0
   (d/(label+'.txt')).write_text(out.stdout+out.stderr)
  r['changed_tracked_files']=subprocess.check_output(['git','diff','HEAD','--name-only'],cwd=repo,text=True).splitlines()
  r['docs']={str(f.relative_to(repo)):hashlib.sha256(f.read_bytes()).hexdigest() for f in sorted((repo/'docs').rglob('*.md'))}
 results.append(r)
pathlib.Path(a.output).write_text(json.dumps(results,ensure_ascii=False,indent=2)+'\n')
print(json.dumps({'trajectories':len(results),'completed':sum(r['completed'] for r in results),'test_suites_passed':sum(r.get('test_suite_passed',False) for r in results),'independent_checks_passed':sum(r.get('independent_checks_passed',False) for r in results)},indent=2))
