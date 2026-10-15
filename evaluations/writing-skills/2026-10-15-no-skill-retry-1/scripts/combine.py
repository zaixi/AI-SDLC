from pathlib import Path
import json
ROOT=Path(__file__).resolve().parents[1]
parent=Path(json.loads((ROOT/'protocol.json').read_text())['parent'])
rows=[]
for source in [parent,ROOT]:
 for row in json.loads((source/'review/metrics.json').read_text()):
  row['source_root']=str(source)
  if source==ROOT:row['sample']='B'+row['sample'][1:]
  rows.append(row)
(ROOT/'review/combined-metrics.json').write_text(json.dumps(rows,ensure_ascii=False,indent=2)+'\n')
print('Combined',len(rows),'outputs without changing historical files')
