"""Post-run probes prompted by static review; not part of frozen scoring checks."""
from pathlib import Path
import json,subprocess
ROOT=Path(__file__).resolve().parents[1]
PROBES={
'E01':'''import json,sqlite3,tempfile,sys
from pathlib import Path
sys.path.insert(0,"/work")
import import_billing as m
out={}
for scenario in ['equal_legacy_scale','nonfinite_amount']:
 with tempfile.TemporaryDirectory() as tmp:
  db=Path(tmp)/'db'
  with sqlite3.connect(db) as c:
   c.execute('CREATE TABLE billing(id INTEGER PRIMARY KEY,billing_id TEXT NOT NULL,amount TEXT NOT NULL,billing_date TEXT NOT NULL)')
   if scenario=='equal_legacy_scale':c.executemany('INSERT INTO billing(billing_id,amount,billing_date) VALUES (?,?,?)',[('a','12.30','2026-10-01'),('a','12.3','2026-10-01')])
  body='billing_id,amount,billing_date\\n'+('b,1,2026-10-01\\n' if scenario=='equal_legacy_scale' else 'a,NaN,2026-10-01\\n')
  try:m.import_csv(db,body);status='accepted'
  except Exception as e:status=type(e).__name__+': '+str(e)
  with sqlite3.connect(db) as c:rows=c.execute('SELECT billing_id,amount,billing_date FROM billing').fetchall()
  out[scenario]={'status':status,'rows':rows}
print(json.dumps(out))
''',
'E02':'''import json,tempfile,subprocess,sys
from pathlib import Path
with tempfile.TemporaryDirectory() as tmp:
 source=Path(tmp)/'in';dest=Path(tmp)/'out'
 source.write_text(''.join(json.dumps({'service':'a','status':200,'duration_ms':x})+'\\n' for x in [1,2,2]))
 p=subprocess.run([sys.executable,'/work/summarize.py',str(source),str(dest)],capture_output=True,text=True)
 print(json.dumps({'exit':p.returncode,'csv':dest.read_text() if dest.exists() else None,'expected_mean':5/3}))
'''}
results=[]
for run in sorted((ROOT/'runs').glob('*')):
 case=run.name.split('-')[0]
 cmd=['bwrap','--die-with-parent','--unshare-all','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64','--ro-bind','/etc/alternatives','/etc/alternatives','--proc','/proc','--dev','/dev','--tmpfs','/tmp','--ro-bind',str(run/'work'),'/work','--chdir','/work','--','/usr/bin/python3','-c',PROBES[case]]
 p=subprocess.run(cmd,capture_output=True,text=True,timeout=20)
 results.append({'id':run.name,'exit':p.returncode,'stdout':p.stdout,'stderr':p.stderr})
(ROOT/'review/diagnostics.json').write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False,indent=2))
