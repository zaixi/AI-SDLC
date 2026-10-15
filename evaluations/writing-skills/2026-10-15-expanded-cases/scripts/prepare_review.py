"""Anonymize complete outputs and summarize evidence without assigning quality scores."""
from pathlib import Path
import hashlib, json, random, re
ROOT=Path(__file__).resolve().parents[1]
runs=sorted((ROOT/'runs').glob('*/result.json'))
rows=[]
for f in runs:
 r=json.loads(f.read_text());folder=f.parent
 events=[]
 for line in (folder/'events.jsonl').read_text().splitlines():
  try:events.append(json.loads(line))
  except ValueError:pass
 texts=[e['part']['text'] for e in events if e.get('type')=='text']
 final=texts[-1] if texts else ''
 visible='\n\n'.join(texts)
 cli_visible_chars=len(visible)
 output_source='opencode_text'
 if not texts:
  for response in sorted(folder.glob('response-*.txt'),reverse=True):
   chunks=[];finished=False
   for line in response.read_text().splitlines():
    if not line.startswith('data: '):continue
    try: data=json.loads(line[6:])
    except ValueError:continue
    for choice in data.get('choices',[]):
     chunks.append(choice.get('delta',{}).get('content') or '')
     finished=finished or choice.get('finish_reason')=='stop'
   if finished and ''.join(chunks):
    final=visible=''.join(chunks);output_source='provider_final_missing_in_cli'
    (folder/'recovered-provider-final.md').write_text(final+'\n');break
 calls=[]
 for e in events:
  if e.get('type')=='tool_use':
   part=e.get('part',{});state=part.get('state',{});calls.append({'tool':part.get('tool'),'input':state.get('input'),'status':state.get('status')})
 usages=[json.loads(p.read_text()) for p in folder.glob('usage-*.json')]
 token_sums={key:sum(u.get('usage',{}).get(key,0) for u in usages) for key in ['prompt_tokens','completion_tokens','total_tokens']}
 usage_records=sum(bool(u.get('usage')) for u in usages)
 requests=[]
 for q in sorted(folder.glob('request-*.json')):
  d=json.loads(q.read_text())
  if d.get('tools'):requests.append({key:d.get(key) for key in ['model','reasoning_effort','max_tokens','temperature']})
 artifacts=[{'path':str(p.relative_to(folder/'work')),'text':p.read_text()} for p in sorted((folder/'work').rglob('*')) if p.is_file() and p.suffix in ('.md','.txt')]
 rows.append({'output_source':output_source,'cli_visible_chars':cli_visible_chars,'artifacts':artifacts,'artifact_chars':sum(len(x['text']) for x in artifacts),'case':r['case'],'condition':r['condition'],'run_id':r['id'],'exit':r['exit'],'seconds':r['seconds'],'model_requests':r['model_requests'],'has_text':r['has_text'],'visible_chars':len(visible),'final_chars':len(final),'final_english_words':len(re.findall(r"\b[\w'-]+\b",final)),'text_messages':len(texts),'tool_calls':calls,'token_usage_recorded':token_sums,'usage_records':usage_records,'wire_settings':requests,'final':final,'visible':visible})
random.Random(932167).shuffle(rows)
review=ROOT/'review';anon=review/'anonymous';anon.mkdir(exist_ok=True)
mapping={};metrics=[]
for i,row in enumerate(rows,1):
 label=f'S{i:02}'
 mapping[label]={'condition':row['condition'],'case':row['case'],'run_id':row['run_id']}
 (anon/(label+'.md')).write_text('# '+label+' / '+row['case']+'\n\n'+row['visible']+'\n'+''.join('\n\n## 附带文件：'+a['path']+'\n\n'+a['text'] for a in row['artifacts']))
 metrics.append({**{k:v for k,v in row.items() if k not in ['final','visible','artifacts']},'sample':label})
(review/'mapping.json').write_text(json.dumps(mapping,ensure_ascii=False,indent=2)+'\n')
(review/'metrics.json').write_text(json.dumps(metrics,ensure_ascii=False,indent=2)+'\n')
for case in sorted({r['case'] for r in rows}):
 selected=[(label,info) for label,info in mapping.items() if info['case']==case]
 (review/(case+'-anonymous.md')).write_text('\n\n---\n\n'.join((anon/(label+'.md')).read_text() for label,_ in selected))
print(json.dumps({'completed_records':len(rows),'text_outputs':sum(x['has_text'] for x in rows),'anonymous_groups':sorted({r['case'] for r in rows})}))
