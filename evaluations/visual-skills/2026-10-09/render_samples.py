from pathlib import Path
import re,json,subprocess,concurrent.futures
p=Path('/tmp/ai-sdlc-visual-bench');out=p/'rendered';out.mkdir(exist_ok=True)
(p/'puppeteer.json').write_text(json.dumps({'executablePath':'/usr/bin/chromium','args':['--no-sandbox','--disable-dev-shm-usage']}))
sources=[('show-me',Path('/tmp/show-me-ca7c8088.md')),('visual-explanation-reference',Path('/workspace/AI-SDLC/skills/visual-explanation/references/diagram-patterns.md')),('mermaid-root',p/'softaworks-mermaid.md')]+[(f'mermaid-reference-{f.stem}',f) for f in sorted((p/'mermaid-skill/references').glob('*.md'))]
jobs=[]
for name,f in sources:
 blocks=re.findall(r'```mermaid\s*\n(.*?)```',f.read_text(),re.S)
 selected=blocks if 'reference-' not in name or name=='visual-explanation-reference' else blocks[:1]
 for i,s in enumerate(selected,1):
  if s.strip().startswith('diagramType'):continue
  stem=f'{name}-{i}';(out/(stem+'.mmd')).write_text(s);jobs.append((stem,str(f)))
def run(item):
 stem,source=item
 r=subprocess.run([str(p/'node_modules/.bin/mmdc'),'-p',str(p/'puppeteer.json'),'-i',str(out/(stem+'.mmd')),'-o',str(out/(stem+'.svg'))],capture_output=True,text=True,timeout=40)
 (out/(stem+'.log')).write_text(r.stdout+r.stderr)
 return dict(id=stem,source=source,passed=r.returncode==0,exit_code=r.returncode,diagnostic=(r.stdout+r.stderr)[-1200:])
results=list(concurrent.futures.ThreadPoolExecutor(max_workers=3).map(run,jobs));(p/'render-results.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps([dict(id=x['id'],passed=x['passed']) for x in results],ensure_ascii=False));print('passed',sum(x['passed'] for x in results),'/',len(results))
