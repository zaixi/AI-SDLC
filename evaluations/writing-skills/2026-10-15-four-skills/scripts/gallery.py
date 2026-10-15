"""Build a local, offline comparison page from the untouched model outputs."""
from pathlib import Path
import html,json
import markdown
ROOT=Path(__file__).resolve().parents[1]
NAMES={'clear':'writing-clearly-and-concisely','humanizer':'humanizer','ste':'asd-ste100','adhd':'i-have-adhd'}
def md(text):
 return markdown.markdown(text.replace('<','&lt;').replace('>','&gt;'),extensions=['fenced_code','tables'])
metrics=json.loads((ROOT/'review/metrics.json').read_text())
cases=json.loads((ROOT/'inputs/cases.json').read_text())['cases']
sections=[]
for case in cases:
 cards=[]
 for row in sorted((r for r in metrics if r['case']==case['id']),key=lambda r:r['sample']):
  folder=ROOT/'runs'/row['run_id'];text=(folder/('recovered-provider-final.md' if row['output_source']=='provider_final_missing_in_cli' else 'answer.md')).read_text();files=[]
  for p in sorted((folder/'work').rglob('*')):
   if p.is_file() and p.suffix in ('.md','.txt'):
    files.append('<details open><summary>模型附带文件：'+html.escape(str(p.relative_to(folder/'work')))+'</summary>'+md(p.read_text())+'</details>')
  card='<article><h2>'+row['sample']+' <span class="identity" hidden>'+NAMES[row['condition']]+'</span></h2>'
  card+='<p class="metrics">回复 '+str(row['visible_chars'])+' 字符 · 文件 '+str(row['artifact_chars'])+' 字符 · '+str(row['seconds'])+' 秒</p>'
  card+=('<p>交付异常：以下为服务端已完成、CLI 漏记的终稿。</p>' if row['output_source']=='provider_final_missing_in_cli' else '')+md(text)+''.join(files)+'</article>';cards.append(card)
 sections.append('<section class="case" id="'+case['id']+'"><h2>'+case['id']+' · '+case['type']+'</h2><details><summary>原题</summary>'+md(case['prompt'])+'</details><div class="grid">'+''.join(cards)+'</div></section>')
page='''<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>四个写作 Skill · 原始输出比较</title><style>
*{box-sizing:border-box}body{margin:0;background:#f3f5f7;color:#202734;font:16px/1.65 system-ui,sans-serif}main{max-width:1520px;margin:auto;padding:24px}h1{font-size:27px}h2{font-size:20px}.grid{display:grid;grid-template-columns:repeat(2,minmax(0,1fr));gap:18px}article{background:white;border:1px solid #d6dce5;padding:22px;border-radius:8px;overflow-wrap:anywhere}article h2{border-bottom:1px solid #ddd;padding-bottom:10px}article h3{font-size:17px}p.metrics{font-size:13px;color:#586578}pre{overflow:auto;padding:12px;background:#f5f6f8;line-height:1.4}code{font-size:14px}table{border-collapse:collapse;width:100%}td,th{border:1px solid #ddd;padding:7px;text-align:left}details{margin:14px 0;padding:12px;background:#fafafa}summary{cursor:pointer}nav{position:sticky;top:0;background:#eef2f6;padding:12px;display:flex;gap:14px;align-items:center;z-index:1}button{padding:8px 16px;border:1px solid #bdc9d8;background:white;border-radius:5px;cursor:pointer}button.active{background:#1c4d78;color:white}.identity{font-size:14px;color:#395b78}.case[hidden]{display:none}@media(max-width:850px){.grid{grid-template-columns:1fr}main{padding:12px}}
</style><main><h1>四个写作 Skill：原始输出比较</h1><p>DeepSeek Flash / OpenCode · 3 题 × 4 组，每组一次。先看回答，再揭示身份。未修改模型正文；回复和模型附带文件分别展示。字符数包含 Markdown，不能直接当质量分。</p><nav>'''
page+=''.join('<button data-case="'+c['id']+'">'+c['id']+'</button>' for c in cases)
page+='''<label><input type="checkbox" id="reveal">显示 Skill 名称</label></nav>'''+''.join(sections)+'''<script>
function selectCase(id){document.querySelectorAll('.case').forEach(x=>x.hidden=x.id!==id);document.querySelectorAll('[data-case]').forEach(x=>x.classList.toggle('active',x.dataset.case===id));}document.querySelectorAll('[data-case]').forEach(x=>x.addEventListener('click',()=>selectCase(x.dataset.case)));document.getElementById('reveal').addEventListener('change',e=>document.querySelectorAll('.identity').forEach(x=>x.hidden=!e.target.checked));selectCase('C01');
</script></main></html>'''
(ROOT/'gallery.html').write_text(page)
print('gallery.html')
