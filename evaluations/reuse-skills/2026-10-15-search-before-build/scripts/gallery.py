from pathlib import Path
import json,html
ROOT=Path(__file__).resolve().parents[1]
esc=html.escape
parts=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>Real architecture skill comparison</title><style>body{font:16px system-ui;margin:2rem;color:#17202a}main{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:1rem}article{border:1px solid #ccc;padding:1rem;min-width:0}pre{white-space:pre-wrap;overflow-wrap:anywhere;font:14px/1.5 ui-monospace}h1{font-size:24px}summary{cursor:pointer;padding:.5rem;background:#f0f3f6}@media(max-width:850px){main{grid-template-columns:1fr}}</style><h1>search-first 与 search-before-build：五题比较</h1><p>OpenCode + deepseek-flash；每题每组一次；原始输出，未润色。文件内容以纯文本展示。</p>']
for case in json.loads((ROOT/'inputs/cases.json').read_text())['cases']:
 parts.append('<h2>'+esc(case['id']+' '+case['title'])+'</h2><p>'+esc(case['prompt'])+'</p><main>')
 for condition in ['search-first','search-before-build']:
  run=ROOT/'runs'/(case['id']+'-'+condition)
  if not (run/'result.json').exists():continue
  result=json.loads((run/'result.json').read_text());parts.append('<article><h3>'+esc(condition)+'</h3><p>'+esc(str(result['exit']))+' exit / '+str(result['seconds'])+' s / '+str(result['output_tokens'])+' output tokens</p>')
  parts.append('<p><strong>'+('已生成目标文件' if (run/'work'/({'R01':'inventory/export.py','R02':'pack.py','R03':'recommendation.md','A01':'design.md','A02':'design.md'}[case['id']])).exists() else '未生成目标文件')+('；预算耗尽' if result.get('budget_exhausted') else '')+'</strong></p>')
  parts.append('<details open><summary>最后一段回复（不代表已完成）</summary><pre>'+esc((run/'final.md').read_text())+'</pre></details>')
  for name in ['design.md','recommendation.md','pack.py','inventory/export.py']:
   p=run/'work'/name
   if p.exists():parts.append('<details><summary>'+esc(name)+'</summary><pre>'+esc(p.read_text())+'</pre></details>')
  parts.append('<details><summary>完整可见文字（含过程说明）</summary><pre>'+esc((run/'answer.md').read_text())+'</pre></details></article>')
 parts.append('</main>')
parts.append('</html>');(ROOT/'gallery.html').write_text(''.join(parts))
