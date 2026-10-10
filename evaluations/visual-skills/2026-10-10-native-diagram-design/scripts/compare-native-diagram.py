import argparse,concurrent.futures,hashlib,json,os,re,shutil,socket,struct,subprocess,tempfile,uuid
from pathlib import Path
from urllib.parse import urlsplit

REPO=Path('/workspace/AI-SDLC');SOURCE=REPO/'evaluations/visual-skills/2026-10-09-challenge';BASE=REPO/'evaluations/visual-skills/2026-10-10-native-diagram-design'
CLI=Path('/tmp/visual-compare-cli/node_modules/@openai/codex-linux-x64/vendor/x86_64-unknown-linux-musl/bin/codex')
NODE=Path(shutil.which('node')).resolve();TOOLS=Path('/tmp/visual-small-render-tools');IMAGE='visual-small-browser:local'
AUTH=json.loads(Path('/tmp/visual-device-login-state.json').read_text())['volume']
ORDER=[('show-me','01-mixed'),('v042','01-mixed'),('diagram-design','01-mixed'),('diagram-design','02-c4'),('v042','02-c4'),('show-me','02-c4')]
PYTHON_IMAGE='python@sha256:34386ef0cb081344d7ec1c103ba398e6e9f64e9ab3a1509accc92a4e24a07258'

def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def run(args,**kwargs):return subprocess.run(args,text=True,capture_output=True,check=True,**kwargs)
def artifacts(text):return re.findall(r'```(mermaid|html)\s*\n([\s\S]*?)```',text)
def save_json(p,data):p.parent.mkdir(parents=True,exist_ok=True);p.write_text(json.dumps(data,ensure_ascii=False,indent=2)+'\n')

def common_container(name):
 return ['docker','run','-d','--rm','--name',name,'--user','1000:1000','--cap-drop','ALL','--security-opt','no-new-privileges','--read-only','--tmpfs','/tmp:rw,nosuid,size=256m','--tmpfs','/home/renderer:rw,nosuid,uid=1000,gid=1000,mode=700']

def execute_model(container,prompt,record_dir,thread=None,images=None):
 args=['docker','exec',container,'codex','--no-daemon','exec','--ignore-user-config','--skip-git-repo-check','--sandbox','read-only','-C','/input','--json']
 if thread:
  args+=['resume','--json','--ignore-user-config','--skip-git-repo-check']
  for image in images or []:args+=['-i','/feedback/'+image.name]
  args += [thread,prompt]
 else:args += [prompt]
 p=subprocess.run(args,text=True,capture_output=True,stdin=subprocess.DEVNULL,timeout=600)
 record_dir.mkdir(parents=True,exist_ok=True)
 (record_dir/'events.jsonl').write_text(p.stdout);(record_dir/'stderr.txt').write_text(p.stderr);(record_dir/'prompt.txt').write_text(prompt)
 events=[]
 for line in p.stdout.splitlines():
  try:events.append(json.loads(line))
  except json.JSONDecodeError:pass
 starts=[e['thread_id'] for e in events if e.get('type')=='thread.started']
 answers=[e['item'].get('text','') for e in events if e.get('type')=='item.completed' and e.get('item',{}).get('type')=='agent_message']
 info={'exit_code':p.returncode,'thread_id':starts[-1] if starts else thread,'usage':[e.get('usage') for e in events if e.get('type')=='turn.completed'],'completed_item_types':[e.get('item',{}).get('type') for e in events if e.get('type')=='item.completed']}
 save_json(record_dir/'status.json',info)
 if p.returncode or not answers:raise RuntimeError('Model call failed; recorded, not silently replaced.')
 return answers[-1],info

def render_stage(renderer,work,out,text,stage):
 result=[];pics=[];srcs=artifacts(text)
 if not srcs:raise RuntimeError('No Mermaid or HTML artifacts in this stage; recorded, not replaced.')
 for i,(kind,source) in enumerate(srcs,1):
  if kind=='html':
   rec,images=render_html(renderer,work,out,source,stage,i);result.append(rec);pics.extend(images);continue
  name=f'{stage}-{i}';mmd=work/(name+'.mmd');mmd.write_text(source)
  rec={'block':i,'type':source.splitlines()[0],'format':'mermaid','source_sha256':sha(mmd)}
  for ext in ['svg','png']:
   target=out/(name+'.'+ext)
   args=['docker','exec',renderer,'/usr/local/bin/node','/opt/render-tools/node_modules/@mermaid-js/mermaid-cli/src/cli.js','-p','/work/puppeteer.json','-i','/work/'+mmd.name,'-o','/out/'+target.name,'--size','1600','--no-font-embed','-b','white']
   p=subprocess.run(args,text=True,capture_output=True,timeout=90)
   rec[ext]={'status':'passed' if p.returncode==0 and target.exists() else 'failed','exit_code':p.returncode,'diagnostic':(p.stdout+p.stderr)[-2200:]}
   if target.exists():
    rec[ext]['file']=target.name
    if ext=='png':rec[ext]['pixels']=struct.unpack('>II',target.read_bytes()[16:24]);pics.append(target)
  result.append(rec)
 save_json(out/(stage+'-render.json'),result)
 return result,pics


def render_html(renderer,work,out,source,stage,index):
 name=f'{stage}-{index}';path=work/(name+'.html');path.write_text(source)
 rec={'block':index,'format':'html','type':'HTML with inline SVG','source_sha256':sha(path)}
 args=['docker','exec',renderer,'/usr/local/bin/node','/work/render-native-html.cjs','/work/'+path.name,'/out/'+name]
 p=subprocess.run(args,text=True,capture_output=True,timeout=120)
 rec['png']={'status':'passed' if p.returncode==0 else 'failed','exit_code':p.returncode,'diagnostic':(p.stdout+p.stderr)[-2500:]}
 pics=[];receipt=out/(name+'-browser.json')
 if receipt.exists():
  browser=json.loads(receipt.read_text());rec['browser']=browser
  pics=[out/x['file'] for x in browser['diagrams']]
  pics.append(out/(name+'-desktop.png'))
  rec['png']['file']=name+'-desktop.png';rec['svg_images']=[x['file'] for x in browser['diagrams']]
  rec['mobile_file']=name+'-mobile.png'
 rec['checks']={}
 for label,script in [('self_check',BASE/'inputs/diagram-design/scripts/self_check.py'),('geometry',BASE/'inputs/verify-geometry.py')]:
  args=['docker','run','--rm','--network','none','--cap-drop','ALL','--security-opt','no-new-privileges','--read-only','--user','1000:1000','--env','PYTHONDONTWRITEBYTECODE=1','--mount',f'type=bind,src={BASE/"inputs/diagram-design"},dst=/skill,readonly','--mount',f'type=bind,src={BASE/"inputs/verify-geometry.py"},dst=/geometry.py,readonly','--mount',f'type=bind,src={work},dst=/work,readonly',PYTHON_IMAGE,'python']
  args+=['/skill/scripts/self_check.py','--offline','/work/'+path.name] if label=='self_check' else ['/geometry.py','/work/'+path.name]
  check=subprocess.run(args,text=True,capture_output=True,timeout=60)
  rec['checks'][label]={'status':'passed' if check.returncode==0 else 'failed','exit_code':check.returncode,'diagnostic':(check.stdout+check.stderr)[-6000:]}
 return rec,pics

def model_metadata(container):
 p=run(['docker','exec',container,'sh','-c','find /home/renderer/.codex/sessions -name "*.jsonl" -type f -exec cat {} +'])
 result=[]
 for line in p.stdout.splitlines():
  try:e=json.loads(line)
  except json.JSONDecodeError:continue
  if e.get('type')=='turn_context':
   data=e.get('payload',{});result.append({k:data[k] for k in ['model','model_provider','effort','reasoning_effort'] if k in data})
 return result

def main():
 if BASE.exists():raise SystemExit('Output already exists; do not overwrite samples.')
 (BASE/'inputs').mkdir(parents=True)
 shutil.copytree(REPO/'skills/visual-explanation',BASE/'inputs/v042')
 (BASE/'inputs/show-me').mkdir()
 shutil.copy(REPO/'skills/visual-explanation/references/show-me.upstream.md',BASE/'inputs/show-me/SKILL.md')
 shutil.copy(REPO/'skills/visual-explanation/LICENSE',BASE/'inputs/show-me/LICENSE')
 shutil.copytree(SOURCE/'inputs/mermaid-diagrams',BASE/'inputs/mermaid-diagrams');shutil.copy(SOURCE/'inputs/prompts.json',BASE/'inputs/prompts.json')
 shutil.copytree('/tmp/diagram-design-inspection/skills/diagram-design',BASE/'inputs/diagram-design-upstream')
 shutil.copy('/tmp/diagram-design-inspection/LICENSE',BASE/'inputs/diagram-design-upstream/LICENSE')
 shutil.copytree(BASE/'inputs/diagram-design-upstream',BASE/'inputs/diagram-design')
 guide=BASE/'inputs/diagram-design/references/style-guide.md';guide.write_text(guide.read_text().replace('Font source: `web`','Font source: `system`'))
 shutil.copy('/tmp/diagram-design-inspection/scripts/verify-geometry.py',BASE/'inputs/verify-geometry.py')
 shutil.copy('/tmp/diagram-design-inspection/source.json',BASE/'inputs/diagram-design-source.json')
 rubric=json.loads((SOURCE/'rubric.json').read_text());rubric['feedback_checks']=['Initial vs final layout and labels','Preserve all confirmed relationships, states and constraints','Distinguish rendering success from readability','Report remaining issues honestly','Do not claim changed source has already been inspected']
 save_json(BASE/'rubric.json',rubric)
 save_json(BASE/'protocol.json',{'conditions':['show-me','v042','diagram-design'],'tasks':['01-mixed','02-c4'],'trajectories_per_condition':2,'total_trajectories':6,'model_calls_per_trajectory':3,'order':ORDER,'input':'Same tasks and feedback. Pinned show-me alone; v042 plus Mermaid guide; diagram-design plus its references and templates. Native Mermaid or static offline HTML/SVG allowed for all groups. Full text injection, not native discovery. Effective diagram-design style differs only by Font source: system; original preserved.','feedback':'Actual PNG images plus renderer status, no reviewer correction hints. Two equally worded feedback opportunities per trajectory. Final changed sources rendered independently without more model feedback.','generation':'One isolated container per trajectory, --no-daemon, own tmpfs home and local-only resume history. No parent/repo/peer mount. Own images readonly; shared login-only auth volume readonly.','renderer':'Independent network-none container, readonly root/input/tools, writable own output/tmpfs, no auth or Docker socket mount. Chromium Puppeteer external-container configuration as previously validated.','model':'CLI 0.162.0 default, no override; serving model from local turn_context if available.','limits':['One sample per case/condition','Externally orchestrated rendering; does not test agent choosing a native render tool','Static offline HTML only; no animation or remote fonts','Two feedback opportunities, not unlimited polish','Root unblinded review; not a user study'],'sampling':'No random seed or sampling controls; counterbalanced condition order by task.'})
 save_json(BASE/'input-manifest.json',{str(p.relative_to(BASE)):sha(p) for p in (BASE/'inputs').rglob('*') if p.is_file()})
 prompts=json.loads((BASE/'inputs/prompts.json').read_text());records=[]
 for condition,case in ORDER:
  trajectory=BASE/'trajectories'/condition/case;trajectory.mkdir(parents=True)
  print('START',condition,case,flush=True)
  with tempfile.TemporaryDirectory(prefix='visual-feedback-') as scratch:
   root=Path(scratch);assigned=root/'input';work=root/'render-work';out=root/'images'
   for d in [assigned,work,out]:d.mkdir()
   shutil.copytree(BASE/'inputs'/condition,assigned/'skill')
   if condition=='v042':shutil.copytree(BASE/'inputs/mermaid-diagrams',assigned/'mermaid-diagrams')
   (assigned/'task.txt').write_text(prompts[case])
   shutil.copy('/tmp/render-native-html.cjs',work/'render-native-html.cjs')
   (work/'puppeteer.json').write_text(json.dumps({'executablePath':'/usr/bin/chromium','args':['--no-sandbox','--disable-setuid-sandbox']}))
   generation='visual-generation-'+uuid.uuid4().hex[:12];renderer='visual-render-'+uuid.uuid4().hex[:12]
   g=common_container(generation)+['--mount',f'type=bind,src={assigned},dst=/input,readonly','--mount',f'type=bind,src={out},dst=/feedback,readonly','--mount',f'type=volume,src={AUTH},dst=/credentials,readonly']
   for name in ['codex','codex-code-mode-host']:g+=['--mount',f'type=bind,src={CLI.with_name(name)},dst=/usr/local/bin/{name},readonly']
   for name in ['HTTPS_PROXY','HTTP_PROXY','NO_PROXY']:
    if name in os.environ:g+=['--env',name]
   route=urlsplit(os.environ.get('HTTPS_PROXY') or os.environ.get('HTTP_PROXY',''))
   if route.hostname:g+=['--add-host',f'{route.hostname}:{socket.gethostbyname(route.hostname)}']
   cert=os.environ.get('CODEX_PROXY_CERT')
   if cert:g+=['--mount',f'type=bind,src={cert},dst=/etc/ssl/certs/platform.pem,readonly','--env','SSL_CERT_FILE=/etc/ssl/certs/platform.pem']
   g+=['--entrypoint','sh',IMAGE,'-c','mkdir /home/renderer/.codex; ln -s /credentials/auth.json /home/renderer/.codex/auth.json; exec tail -f /dev/null']
   r=common_container(renderer)+['--network','none','--mount',f'type=bind,src={work},dst=/work,readonly','--mount',f'type=bind,src={out},dst=/out','--mount',f'type=bind,src={TOOLS},dst=/opt/render-tools,readonly','--mount',f'type=bind,src={NODE},dst=/usr/local/bin/node,readonly','--entrypoint','tail',IMAGE,'-f','/dev/null']
   try:
    run(g);run(r)
    prompt='Apply the primary skill to the task below. Choose the native output format that fits the skill and task: Markdown with editable Mermaid blocks, or one complete static self-contained HTML document with inline SVG in a fenced html block. Include brief necessary prose/tables. All output must work offline with system font fallbacks, no external resources or animation. A rendering service is available through this test controller: first return the current draft; actual images of that draft will then be appended in this same conversation. Further rendered feedback will be supplied if you change the draft. The operator has configured the evaluation style and canvas: shipped colors, offline font source, doc-wide if an HTML diagram needs a size preset. No client branding is requested. State the chosen views and size briefly, then generate this draft without waiting for another reply. This is one authorized comparison task, not an installation or client onboarding. Do not invoke tools, install packages, fetch resources, delegate, save profiles or read credentials. Do not discuss test/skill names. Do not redesign the supplied system. Reply in Chinese.\n<primary_skill>\n'+(assigned/'skill/SKILL.md').read_text()+'\n</primary_skill>\n'
    if condition=='diagram-design':
     refs=['style-guide.md','profiles.md','output-spec.md','layout-budget.md','primitives-core.md','semantic-patterns.md']
     refs+=['type-architecture.md','type-sequence.md','type-state.md','type-flowchart.md'] if case=='01-mixed' else ['type-architecture.md','type-deployment.md']
     for ref in refs:prompt+='\n<related_reference name="'+ref+'">\n'+(assigned/'skill/references'/ref).read_text()+'\n</related_reference>\n'
     prompt+='\n<template name="template.html">\n'+(assigned/'skill/assets/template.html').read_text()+'\n</template>\n'
    if condition=='v042':
     prompt+='\n<mermaid_guide>\n'+(assigned/'mermaid-diagrams/SKILL.md').read_text()+'\n</mermaid_guide>\n'
     refs=['sequence-diagrams.md','flowcharts.md'] if case=='01-mixed' else ['c4-diagrams.md','advanced-features.md']
     for ref in refs:prompt+='\n<related_reference>\n'+(assigned/'mermaid-diagrams/references'/ref).read_text()+'\n</related_reference>\n'
    prompt+='\n<task>\n'+prompts[case]+'\n</task>\n'
    draft,info=execute_model(generation,prompt,trajectory/'stage0');(trajectory/'stage0/answer.md').write_text(draft);thread=info['thread_id']
    print('DRAFT',condition,case,flush=True)
    current=draft;stages=[]
    for index in range(2):
     stage='stage'+str(index);render,pics=render_stage(renderer,work,out,current,stage)
     body='以下是你上一次输出的实际渲染结果。图片顺序与源码图块顺序一致。请根据已加载的 Skill 继续当前工作，返回本次完整的可编辑图文。渲染成功仅表示生成了图片。不要调用其他工具。\n'
     if index==1:body+='本轮后续不再向你回传渲染反馈；如果这次改动图源码，请如实区分你已经看到的画面与尚未检查的新稿。\n'
     body+='\n渲染状态：\n'+json.dumps([{'block':x['block'],'format':x['format'],'type':x['type'],'render_status':x['png']['status'],'error':x['png'].get('diagnostic') if x['png']['status']!='passed' else None,'native_checks':x.get('checks'),'image_notes':'For HTML: each SVG image then complete desktop page. External requests blocked.' if x['format']=='html' else 'Actual diagram image.'} for x in render],ensure_ascii=False)
     next_stage=trajectory/('stage'+str(index+1));new,call=execute_model(generation,body,next_stage,thread,pics);(next_stage/'answer.md').write_text(new)
     stages.append({'stage':stage,'render':render,'images_supplied':[p.name for p in pics],'source_changed_after_feedback':artifacts(new)!=artifacts(current)})
     current=new;print('FEEDBACK',index+1,condition,case,flush=True)
    final_changed=artifacts(current)!=artifacts((trajectory/'stage1/answer.md').read_text())
    if final_changed:final_render,_=render_stage(renderer,work,out,current,'stage2')
    else:final_render=stages[-1]['render']
    shutil.copytree(out,trajectory/'rendered');shutil.copytree(work,trajectory/'render-inputs')
    final=BASE/'outputs'/condition;final.mkdir(parents=True,exist_ok=True);(final/(case+'.md')).write_text(current)
    record={'condition':condition,'case':case,'status':'completed','thread_id':thread,'model_context':model_metadata(generation),'draft_sha256':sha(trajectory/'stage0/answer.md'),'final_sha256':sha(final/(case+'.md')),'stages':stages,'final_source_changed':final_changed,'final_render':final_render,'image_id':run(['docker','image','inspect','--format','{{.Id}}',IMAGE]).stdout.strip()}
    records.append(record);save_json(BASE/'runs.json',records);print('DONE',condition,case,flush=True)
   except Exception as e:
    if out.exists() and not (trajectory/'rendered').exists():shutil.copytree(out,trajectory/'rendered')
    if work.exists() and not (trajectory/'render-inputs').exists():shutil.copytree(work,trajectory/'render-inputs')
    records.append({'condition':condition,'case':case,'status':'failed','reason':str(e)});save_json(BASE/'runs.json',records);raise
   finally:
    for name in [generation,renderer]:subprocess.run(['docker','rm','-f',name],capture_output=True,timeout=20)

if __name__=='__main__':main()
