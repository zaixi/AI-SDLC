from pathlib import Path
import json,hashlib,re,difflib
B=Path('/workspace/AI-SDLC/evaluations/visual-skills/2026-10-15-v2-expanded')
def sha(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def diagram_sources(t):
 return [(kind,source if kind in ['mermaid','svg'] else re.findall(r'<(?:svg|style)\b[\s\S]*?</(?:svg|style)>',source)) for kind,source in artifacts(t)]
def artifacts(t):return re.findall(r'```(mermaid|html|svg)\s*\n([\s\S]*?)```',t)
runs=json.loads((B/'runs.json').read_text());metrics=[]
for r in runs:
 if r['status']!='completed':continue
 d=B/'trajectories'/r['condition']/r['case'];a=[(d/f'stage{i}/answer.md').read_text() for i in range(3)]
 source='\n'.join(x[1] for x in artifacts(a[-1]));calls=[json.loads((d/f'stage{i}/status.json').read_text()) for i in range(3)]
 usage={k:sum(u.get(k,0) for c in calls for u in c['usage'] if u) for k in ['input_tokens','cached_input_tokens','output_tokens']}
 changes=[]
 for before,after in zip(a,a[1:]):
  diff=list(difflib.ndiff('\n'.join(x[1] for x in artifacts(before)).splitlines(),'\n'.join(x[1] for x in artifacts(after)).splitlines()))
  changes.append({'added_lines':sum(x.startswith('+ ') for x in diff),'removed_lines':sum(x.startswith('- ') for x in diff)})
 metrics.append({'condition':r['condition'],'case':r['case'],'formats':[x[0] for x in artifacts(a[-1])],'answer_chars':len(a[-1]),'all_fenced_source_chars':sum(len(x[1]) for x in re.findall(r'```([^\n]*)\n([\s\S]*?)```',a[-1])),'source_chars':sum(len(x[1]) for x in artifacts(a[-1])),'source_bytes':sum(len(x[1].encode()) for x in artifacts(a[-1])),'source_lines':len(source.splitlines()),'diagrams':sum(len(x.get('browser',{}).get('diagrams',[])) if x['format'] in ['html','svg'] else 1 for x in r['final_render']),'usage':usage,'revision_diffs':changes,'final_document_source_changed':r['final_source_changed'],'final_changed_after_last_feedback':diagram_sources(a[-1])!=diagram_sources(a[-2])})
for m in metrics:
 r=next(r for r in runs if r.get('condition')==m['condition'] and r.get('case')==m['case'] and r['status']=='completed');d=B/'trajectories'/r['condition']/r['case']/'rendered'
 def pics(items):return [n for x in items for n in x.get('svg_images',[x['png']['file']])]
 old=pics(r['stages'][-1]['render']);final=pics(r['final_render']);m['last_feedback_main_images_identical']=len(old)==len(final) and all(sha(d/a)==sha(d/b) for a,b in zip(old,final))
(B/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
for r in runs:
 if r['status']=='completed':
  p=B/'outputs'/r['condition']/(r['case']+'.md');assert sha(p)==r['final_sha256'];assert p.read_bytes()==(B/'trajectories'/r['condition']/r['case']/'stage2/answer.md').read_bytes()
manifest=json.loads((B/'input-manifest.json').read_text());assert all(sha(B/p)==h for p,h in manifest.items())
(B/'integrity-results.json').write_text(json.dumps({'input_files_verified':len(manifest),'completed_outputs_verified':len(metrics)},ensure_ascii=False,indent=2)+'\n')
print(json.dumps(metrics,ensure_ascii=False,indent=2))
