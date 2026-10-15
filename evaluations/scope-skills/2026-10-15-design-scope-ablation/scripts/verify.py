from pathlib import Path
import difflib
import json
import subprocess

ROOT=Path(__file__).resolve().parents[1]
cases={c['id']:c for c in json.loads((ROOT/'inputs/cases.json').read_text())['cases']}
saved=ROOT/'review/results.json'
results=json.loads(saved.read_text()) if saved.exists() else []
completed={r['id'] for r in results}
for run in sorted((ROOT/'runs').glob('*')):
    if run.name in completed or not (run/'result.json').exists():continue
    result=json.loads((run/'result.json').read_text())
    case=cases[result['case']]
    prefix=['bwrap','--die-with-parent','--unshare-all','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--ro-bind','/etc/alternatives','/etc/alternatives','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--ro-bind',str(run/'work'),'/work','--ro-bind',str(ROOT/'review'),'/review','--chdir','/work','--']
    checks=[]
    for label,args in [('independent',['/usr/bin/python3','/review/checks.py',case['id']]),('repository',['/usr/bin/python3','-m','unittest','discover','-s','tests','-v'])]:
        try:
            p=subprocess.run(prefix+args,capture_output=True,text=True,timeout=60)
            checks.append({'kind':label,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
        except subprocess.TimeoutExpired:
            checks.append({'kind':label,'exit':'timeout'})
    files={str(p.relative_to(run/'work')):p for p in (run/'work').rglob('*') if p.is_file() and '__pycache__' not in p.parts and '.git' not in p.parts}
    changes=[];diff=[]
    for name in sorted(set(files)|set(case['files'])):
        before=case['files'].get(name,'');after=files[name].read_text(errors='replace') if name in files else ''
        if before==after:continue
        changes.append({'path':name,'status':'new' if name not in case['files'] else 'deleted' if name not in files else 'modified','lines':len(after.splitlines()),'chars':len(after)})
        diff.extend(difflib.unified_diff(before.splitlines(True),after.splitlines(True),fromfile='before/'+name,tofile='after/'+name))
    (ROOT/'review'/(run.name+'.diff')).write_text(''.join(diff))
    requests=[json.loads(p.read_text()) for p in run.glob('request-*.json')]
    usage=[json.loads(p.read_text()).get('usage',{}) for p in run.glob('usage-*.json')]
    record={k:result[k] for k in ['id','case','condition','exit','seconds','model_requests','output_tokens','budget_exhausted']}
    record.update(checks=checks,changes=changes,models=sorted(set(q['model'] for q in requests)),reasoning_efforts=sorted(set(q.get('reasoning_effort','') for q in requests)),reported_input_tokens=sum(u.get('prompt_tokens',0) for u in usage),upstream_errors=len(list(run.glob('upstream-error-*.json'))))
    results.append(record)
(ROOT/'review/results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
for r in results:print(json.dumps(r,ensure_ascii=False))
