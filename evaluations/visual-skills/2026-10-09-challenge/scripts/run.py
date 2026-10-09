import argparse,hashlib,json,os,shutil,socket,subprocess,tempfile,uuid
from pathlib import Path
from urllib.parse import urlsplit
# Credentials remain in a login-only Docker volume, never this repository.


def digest(p): return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,**kwargs): return subprocess.run(args,check=True,text=True,capture_output=True,**kwargs)

def main():
    parser=argparse.ArgumentParser()
    parser.add_argument('--source',type=Path,required=True,help='Previous evaluation with inputs and rubric')
    parser.add_argument('--output',type=Path,required=True,help='New directory; existing output is never overwritten')
    parser.add_argument('--auth-volume',required=True,help='Docker volume from successful normal CLI login')
    parser.add_argument('--cli-bin',type=Path,required=True,help='Official Codex native binary; sibling code-mode-host required')
    parser.add_argument('--image',default='visual-skill-file-check:local')
    options=parser.parse_args()
    SOURCE=options.source.resolve(); TARGET=options.output.resolve()
    STATE={'volume':options.auth_volume}
    if TARGET.exists(): raise SystemExit('Target already exists; do not replace previous samples.')
    TARGET.mkdir()
    shutil.copytree(SOURCE/'inputs',TARGET/'inputs')
    for n in ['rubric.json','scripts/parse.mjs']:
        dst=TARGET/n;dst.parent.mkdir(exist_ok=True);shutil.copyfile(SOURCE/n,dst)
    prompts=json.loads((TARGET/'inputs/prompts.json').read_text())
    records=[]
    manifest={str(p.relative_to(TARGET)):digest(p) for p in (TARGET/'inputs').rglob('*') if p.is_file()}
    (TARGET/'input-manifest.json').write_text(json.dumps(manifest,indent=2)+'\n')
    cli=options.cli_bin.resolve()
    for condition in ['show-me','mermaid-diagrams','visual-v041']:
      for case,task in prompts.items():
        with tempfile.TemporaryDirectory(prefix='visual-case-') as scratch:
          root=Path(scratch); assigned=root/'input';assigned.mkdir()
          shutil.copytree(TARGET/'inputs'/condition,assigned/'skill')
          if condition=='visual-v041': shutil.copytree(TARGET/'inputs/mermaid-diagrams',assigned/'mermaid-diagrams')
          (assigned/'task.txt').write_text(task)
          name='visual-case-'+uuid.uuid4().hex
          args=['docker','run','--rm','--name',name,'--user','1000:1000','--cap-drop','ALL','--security-opt','no-new-privileges','--read-only','--tmpfs','/tmp:rw,nosuid,size=128m','--tmpfs','/home/tester:rw,nosuid,uid=1000,gid=1000,mode=700','--tmpfs','/home/tester/.codex:rw,nosuid,uid=1000,gid=1000,mode=700','--mount',f'type=bind,src={assigned},dst=/input,readonly','--mount',f'type=volume,src={STATE["volume"]},dst=/credentials,readonly','--mount',f'type=bind,src={cli},dst=/usr/local/bin/codex,readonly','--mount',f'type=bind,src={cli.with_name("codex-code-mode-host")},dst=/usr/local/bin/codex-code-mode-host,readonly']
          for n in ['HTTPS_PROXY','HTTP_PROXY','NO_PROXY']:
            if n in os.environ: args+=['--env',n]
          route=urlsplit(os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY',''))
          if route.hostname: args+=['--add-host',f'{route.hostname}:{socket.gethostbyname(route.hostname)}']
          cert=os.environ.get('CODEX_PROXY_CERT')
          if cert: args+=['--mount',f'type=bind,src={cert},dst=/etc/ssl/certs/platform.pem,readonly','--env','SSL_CERT_FILE=/etc/ssl/certs/platform.pem']
          instruction='Apply the primary skill below to the task. The guide and relevant reference, when supplied, are already loaded as text in this fresh conversation. Generate directly from the supplied materials; do not use any tools, fetch network resources, install anything, delegate, render or save files. Reply in Chinese with the visual and brief necessary explanation. Do not discuss the test or skill names. Do not redesign the provided system.\n\n<primary_skill>\n'+(assigned/'skill/SKILL.md').read_text()+'\n</primary_skill>\n'
          if condition!='show-me':
            guide=assigned/('mermaid-diagrams' if condition=='visual-v041' else 'skill')
            if condition=='visual-v041': instruction+='\n<mermaid_guide>\n'+(guide/'SKILL.md').read_text()+'\n</mermaid_guide>\n'
            refs=['sequence-diagrams.md','flowcharts.md'] if case=='01-mixed' else ['c4-diagrams.md','advanced-features.md']
            for ref in refs: instruction+='\n<related_reference>\n'+(guide/'references'/ref).read_text()+'\n</related_reference>\n'
          instruction+='\n<task>\n'+task+'\n</task>\n'
          (assigned/'model-input.txt').write_text(instruction)
          saved=TARGET/'model-inputs'/condition;saved.mkdir(parents=True,exist_ok=True)
          (saved/f'{case}.txt').write_text(instruction)
          args+=[options.image,'sh','-c','ln -s /credentials/auth.json /home/tester/.codex/auth.json; exec codex --no-daemon exec --ephemeral --ignore-user-config --skip-git-repo-check --sandbox read-only -C /input --json "$1"','case',instruction]
          out=TARGET/'traces'/condition;out.mkdir(parents=True,exist_ok=True)
          try:
            p=subprocess.run(args,stdin=subprocess.DEVNULL,text=True,capture_output=True,timeout=240)
            (out/f'{case}.jsonl').write_text(p.stdout)
            # Keep CLI diagnostics separate from the untouched model answer.
            (out/f'{case}.stderr.txt').write_text(p.stderr)
            events=[]
            for line in p.stdout.splitlines():
              try:events.append(json.loads(line))
              except json.JSONDecodeError:pass
            answers=[e['item'].get('text','') for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
            record={'condition':condition,'case':case,'exit_code':p.returncode,'container':name,'mount_roles':['assigned input readonly','login-only auth volume readonly','CLI binaries readonly'],'image_id':run(['docker','image','inspect','--format','{{.Id}}',options.image]).stdout.strip(),'input_files':{str(f.relative_to(assigned)):digest(f) for f in assigned.rglob('*') if f.is_file()},'status':'generated' if p.returncode==0 and answers else 'failed'}
            if answers:
              dest=TARGET/'outputs'/condition;dest.mkdir(parents=True,exist_ok=True)
              answer=dest/f'{case}.md';answer.write_text(answers[-1]);record['answer_sha256']=digest(answer)
            records.append(record)
            (TARGET/'runs.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
            print(json.dumps({'condition':condition,'case':case,'status':record['status']},ensure_ascii=False),flush=True)
            if record['status']=='failed': raise SystemExit('Stop: functional prerequisite failed; do not silently replace sample.')
          except subprocess.TimeoutExpired:
            records.append({'condition':condition,'case':case,'status':'timeout'})
            (TARGET/'runs.json').write_text(json.dumps(records,ensure_ascii=False,indent=2)+'\n')
            raise SystemExit('Stop: generation timeout.')
          finally: subprocess.run(['docker','rm','-f',name],capture_output=True,timeout=15)

if __name__=='__main__':main()
