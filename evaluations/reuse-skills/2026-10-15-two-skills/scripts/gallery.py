from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
esc=html.escape
parts=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Reuse skills comparison</title><style>body{font:16px system-ui;margin:2rem;color:#17202a}main{display:grid;grid-template-columns:1fr 1fr;gap:1rem}article{border:1px solid #ccc;padding:1rem;min-width:0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.5 ui-monospace}h1{font-size:24px}summary{cursor:pointer;padding:.5rem;background:#f0f3f6}@media(max-width:850px){main{grid-template-columns:1fr}}</style><h1>search-first vs reuse-before-build</h1><p>OpenCode + deepseek-flash；每题每组一次；原始输出，未润色。文件内容以纯文本展示。</p>']
for case in json.loads((ROOT/'inputs/cases.json').read_text())['cases']:
 parts.append('<h2>'+esc(case['id']+' '+case['title'])+'</h2><p>'+esc(case['prompt'])+'</p><main>')
 for condition in ['search-first','reuse-before-build']:
  run=ROOT/'runs'/(case['id']+'-'+condition)
  if not (run/'result.json').exists():continue
  result=json.loads((run/'result.json').read_text());parts.append('<article><h3>'+esc(condition)+'</h3><p>'+str(result['seconds'])+' s / '+str(result['output_tokens'])+' output tokens</p>')
  parts.append('<details open><summary>最终回复</summary><pre>'+esc((run/'final.md').read_text())+'</pre></details>')
  for name in ['inventory/export.py','pack.py','recommendation.md']:
   p=run/'work'/name
   if p.exists():parts.append('<details><summary>'+esc(name)+'</summary><pre>'+esc(p.read_text())+'</pre></details>')
  parts.append('<details><summary>完整可见文字（含过程说明）</summary><pre>'+esc((run/'answer.md').read_text())+'</pre></details></article>')
 parts.append('</main>')
parts.append('</html>');(ROOT/'gallery.html').write_text(''.join(parts))
