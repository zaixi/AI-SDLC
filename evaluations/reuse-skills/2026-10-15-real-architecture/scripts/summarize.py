from pathlib import Path
import json,collections
r=Path(__file__).resolve().parents[1];results=[]
for d in sorted((r/'runs').glob('*')):
 if not (d/'result.json').exists():continue
 result=json.loads((d/'result.json').read_text());tools=collections.Counter();events=[]
 for line in (d/'events.jsonl').read_text().splitlines():
  try:events.append(json.loads(line))
  except ValueError:pass
 texts=[]
 for e in events:
  p=e.get('part',{})
  if e.get('type')=='tool_use':tools[p.get('tool','unknown')]+=1
  if e.get('type')=='text':texts.append(p.get('text',''))
 requests=[json.loads(p.read_text()) for p in d.glob('request-*.json')]
 usage=[json.loads(p.read_text()).get('usage',{}) for p in d.glob('usage-*.json')]
 wire_calls={}; wire_results=set()
 for request in requests:
  for message in request.get('messages',[]):
   for call in message.get('tool_calls',[]):wire_calls[call['id']]=call.get('function',{}).get('name','unknown')
   if message.get('role')=='tool':wire_results.add(message.get('tool_call_id'))
 all_tools=collections.Counter(wire_calls[x] for x in wire_results if x in wire_calls)
 final=texts[-1] if texts else ''
 (d/'final.md').write_text(final+'\n')
 record={k:result[k] for k in ['id','exit','seconds','model_requests','output_tokens','budget_exhausted']}
 record.update({'reported_prompt_tokens':sum(u.get('prompt_tokens',0) for u in usage),'parent_tools':dict(tools),'all_returned_tools_including_errors':dict(all_tools),'final_chars':len(final),'all_text_chars':sum(map(len,texts)),'models':sorted(set(q.get('model','') for q in requests)),'reasoning_efforts':sorted(set(q.get('reasoning_effort','') for q in requests)),'request_count':len(requests)})
 case=next(c for c in json.loads((r/'inputs/cases.json').read_text())['cases'] if result.get('case')==c['id'])
 record['source_files_unchanged']=all((d/'work'/name).exists() and (d/'work'/name).read_text()==content for name,content in case['files'].items())
 record['design_exists']=(d/'work/design.md').exists()
 record['design_chars']=len((d/'work/design.md').read_text()) if record['design_exists'] else 0
 record['infrastructure_errors']=len(list(d.glob('upstream-error-*.json')))
 results.append(record)
(r/'review/metrics.json').write_text(json.dumps(results,ensure_ascii=False,indent=2));print(json.dumps(results,ensure_ascii=False,indent=2))
