"""Posthoc probe prompted by reading E02's rounding; not a frozen test."""
from pathlib import Path
import json
import subprocess

ROOT = Path(__file__).resolve().parents[1]
code = '''import csv,json,subprocess,sys,tempfile
from pathlib import Path
with tempfile.TemporaryDirectory() as tmp:
    source=Path(tmp)/'input.jsonl'; dest=Path(tmp)/'output.csv'
    source.write_text(''.join(json.dumps(dict(service='api',status=200,duration_ms=x))+'\\n' for x in [1,2,2]))
    result=subprocess.run([sys.executable,'/work/summarize.py',str(source),str(dest)],capture_output=True,text=True)
    print(json.dumps(dict(exit=result.returncode,stderr=result.stderr,csv=dest.read_text() if dest.exists() else None)))
'''
results = {}
for condition in ['without', 'with']:
    work = ROOT / 'runs' / ('E02-' + condition) / 'work'
    args = ['bwrap','--die-with-parent','--unshare-all','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--ro-bind','/etc/alternatives','/etc/alternatives','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--ro-bind',str(work),'/work','--chdir','/work','--','python3','-c',code]
    p = subprocess.run(args, capture_output=True, text=True, timeout=30, check=True)
    results[condition] = json.loads(p.stdout)
(ROOT / 'review/precision-probe.json').write_text(json.dumps(results, ensure_ascii=False, indent=2))
print(json.dumps(results, ensure_ascii=False, indent=2))
