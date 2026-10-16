"""Build a local comparison gallery from reviewed selections; no generation feedback."""
from pathlib import Path
import html,json
ROOT=Path(__file__).resolve().parents[1]
esc=html.escape
rows=json.loads((ROOT/'review/assessments.json').read_text())
metrics={x['id']:x for x in json.loads((ROOT/'review/metrics.json').read_text())}
parts=['<!doctype html><html lang="zh-CN"><meta charset="utf-8"><title>图解工具扩展评测</title><style>body{font:16px/1.6 system-ui;margin:30px;background:#f6f7f9;color:#17212b}main{max-width:1550px;margin:auto}section{background:white;padding:24px;margin:24px 0;border:1px solid #ddd;border-radius:10px}img{display:block;max-width:100%;max-height:1000px;object-fit:contain;object-position:left top;border:1px solid #ddd}a{color:#1758a0}small{color:#52606d}nav a{margin-right:16px}</style><main><h1>visual-explanation / Archify / Fireworks</h1><p>4 题 × 3 组，每格一次。OpenCode + deepseek-flash/high；输出预算 98304，单次 32768，1200 秒。截图为事后评审产物，不代表模型交付 PNG。</p><nav>']
for case in sorted(set(x['case'] for x in rows)):parts.append(f'<a href="#'+esc(case)+'">'+esc(case)+'</a>')
parts.append('</nav>')
for row in rows:
 m=metrics[row['id']]
 parts.append('<section id="'+esc(row['id'])+'"><h2 id="'+esc(row['case'])+'">'+esc(row['id'])+'</h2><p>'+esc(row['verdict'])+'</p><small>'+esc(f"{m['seconds']} s · {m['model_requests']} requests · {m['output_tokens']} output tokens")+'</small><ul>')
 for point in row.get('findings',[]):parts.append('<li>'+esc(point)+'</li>')
 parts.append('</ul>')
 for rel in row.get('artifacts',[]):
  href='runs/'+row['id']+'/work/'+rel
  parts.append('<p><a href="'+esc(href,quote=True)+'">'+esc(rel)+'</a></p>')
 for rel in row.get('images',[]):parts.append('<a href="'+esc(rel,quote=True)+'"><img loading="lazy" src="'+esc(rel,quote=True)+'"></a>')
 parts.append('</section>')
parts.append('</main></html>')
(ROOT/'gallery.html').write_text(''.join(parts))
print(ROOT/'gallery.html')
