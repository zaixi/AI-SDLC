"""One isolated OpenCode session per task and explicitly invoked writing skill."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse, hashlib, json, os, random, shutil, subprocess, tempfile, threading
import relay_base as core
ROOT=Path(__file__).resolve().parents[1]
CONDITIONS=['search-first','reuse-before-build']
core.ROOT=ROOT
core.CONDITIONS=CONDITIONS
core.TIMEOUT=420
core.REQUEST_LIMIT=32
core.OUTPUT_BUDGET=32768

def setup(run,condition,case):
    for rel in ['home/.config/opencode','home/.cache/opencode','work','input','tools']:
        (run/rel).mkdir(parents=True,exist_ok=True)
    for name, content in case.get('files', {}).items():
        target=run/'work'/name; target.parent.mkdir(parents=True,exist_ok=True); target.write_text(content)
    if condition!='none':shutil.copytree(ROOT/'snapshots'/condition,run/'input/skill')
    shutil.copy2(ROOT/'scripts/sandbox_bridge.py',run/'tools/sandbox_bridge.py')
    (run/'home/.cache/opencode/models.json').write_text('{}\n')
    (run/'tools/passwd').write_text(f'eval:x:{os.getuid()}:{os.getgid()}:Evaluation:/home/eval:/bin/bash\n')
    config={'$schema':'https://opencode.ai/config.json','model':'evaluation/'+core.MODEL,'small_model':'evaluation/'+core.MODEL,
      'enabled_providers':['evaluation'],'autoupdate':False,'share':'disabled','snapshot':False,'plugin':[],'instructions':[],
      'provider':{'evaluation':{'npm':'@ai-sdk/openai-compatible','name':'Evaluation relay','options':{'baseURL':'http://127.0.0.1:18761/v1','apiKey':'non-secret-placeholder'},
        'models':{core.MODEL:{'name':core.MODEL,'options':{'reasoningEffort':'high'},'limit':{'context':131072,'output':16384},'modalities':{'input':['text'],'output':['text']}}}}},
      'agent':{'eval':{'description':'Complete the current task','mode':'primary','prompt':core.BASE+'\nPython 3 is available. /work is writable. Public web access is available through webfetch and command-line HTTPS. Node.js and Python 3 are available. Use only public sources; no accounts or credentials are provided.',
        'permission':{'*':'deny','read':'allow','write':'allow','edit':'allow','bash':'allow','glob':'allow','grep':'allow','list':'allow','external_directory':'allow','webfetch':'allow','websearch':'allow','task':'allow'}}},
      'default_agent':'eval','formatter':False,'lsp':False}
    core.write_json(run/'home/.config/opencode/opencode.json',config)
    return config

def command(run,condition,args):
    return ['bwrap','--die-with-parent','--unshare-all','--share-net','--ro-bind','/usr','/usr','--symlink','usr/bin','/bin','--ro-bind','/lib','/lib','--ro-bind','/lib64','/lib64',
      '--proc','/proc','--dev','/dev','--tmpfs','/tmp','--dir','/etc','--ro-bind','/etc/alternatives','/etc/alternatives','--ro-bind','/etc/resolv.conf','/etc/resolv.conf','--ro-bind','/etc/ssl/certs','/etc/ssl/certs',
      '--ro-bind',str(run/'tools/passwd'),'/etc/passwd','--ro-bind',str(core.BINARY),'/opt/opencode',
      '--bind',str(run/'home'),'/home/eval','--bind',str(run/'work'),'/work','--ro-bind',str(run/'input'),'/input',
      '--ro-bind',str(run/'tools'),'/tools','--ro-bind',str(core.SOCKET_PATH),'/run/model.sock','--chdir','/work','--',*args]

def audit_fs(run,condition):
    code='''import json,pathlib,socket
p=pathlib.Path
paths=['/home/liyujiang','/input/skill/SKILL.md','/home/eval/.codex/skills','/home/eval/.agents/skills','/input/specialists','/review','/workspace']
s=socket.socket();s.settimeout(1)
try:s.connect(('1.1.1.1',443));network=True
except OSError:network=False
print(json.dumps({'paths':{x:p(x).exists() for x in paths},'external_network':network,'input_files':[str(x.relative_to('/input')) for x in p('/input').rglob('*') if x.is_file()]}))'''
    p=subprocess.run(command(run,condition,['python3','-c',code]),env=core.environment(),capture_output=True,text=True,check=True,timeout=15)
    result=json.loads(p.stdout)
    assert result['paths']['/input/skill/SKILL.md']==(condition!='none')
    assert not any(v for k,v in result['paths'].items() if k!='/input/skill/SKILL.md')
    # Public networking is enabled equally for both conditions.
    core.write_json(run/'filesystem-audit.json',result)

core.setup=setup
core.command=command
core.audit_fs=audit_fs

def audit_requests(results):
    summaries=[]
    for r in results:
        run=ROOT/'preflight'/r['id']
        body=next(json.loads(p.read_text()) for p in sorted(run.glob('request-*.json')) if json.loads(p.read_text()).get('tools'))
        assert body['model']==core.MODEL
        raw=json.dumps(body)
        assert all(x not in raw for x in ['/home/liyujiang','visual-explanation','oh-my-opencode','skill-creator'])
        summaries.append({'condition':r['condition'],'model':body['model'],'reasoning_effort':body.get('reasoning_effort'),'max_tokens':body.get('max_tokens',body.get('max_completion_tokens')),'tools':[x['function']['name'] for x in body['tools']]})
    core.write_json(ROOT/'preflight/request-audit.json',summaries)

def main():
    parser=argparse.ArgumentParser();parser.add_argument('mode',choices=['audit','probe','run']);parser.add_argument('--model',default='deepseek-flash');args=parser.parse_args()
    core.MODEL=args.model;core.MOCK=args.mode=='audit'
    if not core.MOCK:core.PROVIDER=core.provider()
    with tempfile.TemporaryDirectory(prefix='writing-relay-') as tmp:
        core.SOCKET_PATH=Path(tmp)/'api.sock';server=core.UnixServer(str(core.SOCKET_PATH),core.Relay)
        threading.Thread(target=server.serve_forever,daemon=True).start()
        try:
            if args.mode=='audit':
                jobs=[{'id':'audit-'+c,'condition':c,'prompt':'Reply only OK. Do not use tools.','fixtures':[]} for c in CONDITIONS]
            elif args.mode=='probe':
                jobs=[{'id':'health-'+args.model,'condition':'none','prompt':'Reply only OK. Do not use tools.','fixtures':[]}]
            else:
                assert (ROOT/'preflight/request-audit.json').exists()
                cases=json.loads((ROOT/'inputs/cases.json').read_text())['cases'];jobs=[]
                for case in cases:
                    order=CONDITIONS.copy();random.Random('reuse-20261015-'+case['id']).shuffle(order)
                    jobs.extend({**case,'case':case['id'],'id':case['id']+'-'+c,'condition':c,'repeat':1} for c in order)
                core.write_json(ROOT/'jobs.json',jobs)
                # Existing attempt directories are never retried or overwritten.
                jobs=[j for j in jobs if not (ROOT/'runs'/j['id']).exists()]
            with ThreadPoolExecutor(max_workers=1) as pool:
                results=[f.result() for f in as_completed([pool.submit(core.execute,j,args.mode!='run') for j in jobs])]
            if core.MOCK:audit_requests(results)
        finally:server.shutdown();server.server_close()

if __name__=='__main__':main()
