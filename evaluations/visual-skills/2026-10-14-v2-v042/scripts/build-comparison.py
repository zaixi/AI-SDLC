from pathlib import Path
import json
B=Path('/workspace/AI-SDLC/evaluations/visual-skills/2026-10-14-v2-v042')
runs=[r for r in json.loads((B/'runs.json').read_text()) if r['status']=='completed'];metrics=json.loads((B/'metrics.json').read_text());review=json.loads((B/'content-review.json').read_text());names={'show-me':'show-me','v042':'visual-explanation 0.4.2','candidate':'visual-explanation_2'}
lines=['# visual-explanation_2与 0.4.2：新案例实测','', (B/'conclusion.txt').read_text() if (B/'conclusion.txt').exists() else '结果仍在生成，暂不作总评。','', '每版两题、四条独立容器/会话轨迹，每条两次真实桌面图片反馈。相同模型；两题均允许 Mermaid 或离线 HTML/SVG。可选扩展均不可用，测试回退路径。详见 [协议与限制](README.md)。','', '## 产出规模','', '| 题目 | Skill | 最终图数 | 原生格式 | 图源码字符 | 全部代码块字符 | 三次调用输出 tokens | 最后反馈后仍改图 |','|---|---|---:|---|---:|---:|---:|---|']
for case in ['01-dedup','02-overview']:
 for c in ['v042','candidate']:
  m=next((m for m in metrics if m['condition']==c and m['case']==case),None)
  if m:lines.append(f"| {case} | {names[c]} | {m['diagrams']} | {'HTML/SVG' if 'html' in m['formats'] else 'Mermaid'} | {m['source_chars']:,} | {m['all_fenced_source_chars']:,} | {m['usage']['output_tokens']:,} | {'是，最终画面由评审查看' if m['final_changed_after_last_feedback'] else '否，模型已收到相同图源码的画面'} |")
lines+=['','图数按实际主 SVG/Mermaid 图计数，一份 HTML 可能含多图；伪代码不计作图片，但计入全部代码块。HTML 包含页面样式、文字与表格，Mermaid 源不含外围 Markdown，因此源码字符只反映各自交付物规模。token 是本轮 CLI 用量，含修订，不代表价格或正常按需读取的最低消耗。未测真实需求变更工时。','']
for case,title in [('01-dedup','去重规则与保存、ACK 计数'),('02-overview','14 单元平台：总览与失败影响')]:
 lines+=['## '+title,'']
 if case in review:lines += [review[case].get('judgment',''),'']
 for c in ['v042','candidate']:
  r=next((r for r in runs if r['condition']==c and r['case']==case),None)
  if not r:continue
  d=Path('trajectories')/c/case;lines+=['### '+names[c],'',f'[最终原始回答](outputs/{c}/{case}.md) · [初稿]({d}/stage0/answer.md) · [第一次修订]({d}/stage1/answer.md) · [最终阶段]({d}/stage2/answer.md)','']
  item=review.get(case,{}).get(c,{})
  for k,cn in [('coverage','内容'),('faithfulness','忠实性'),('layout','实际画面'),('validation','检查闭环'),('checker_caveat','检查器限制')]:
   if k in item:lines += [f'**{cn}：** {item[k]}','']
  graph_index=0
  for x in r['final_render']:
   files=x.get('svg_images',[x['png']['file']])
   for file in files:
    graph_index+=1;lines += [f'![{names[c]} {case} 图 {graph_index}]({d}/rendered/{file})','']
   if x['format']=='html':
    stem=x['png']['file'].replace('-desktop.png','');lines += [f'[可编辑 HTML]({d}/render-inputs/{stem}.html) · [完整桌面页]({d}/rendered/{x["png"]["file"]}) · [移动截图]({d}/rendered/{x["mobile_file"]})','', 'GitHub 不直接执行 HTML；下载 HTML 后用浏览器打开即可查看原生页面。','']
   else:
    lines += [f'[可编辑 Mermaid]({d}/render-inputs/{Path(x["png"]["file"]).stem}.mmd) · [SVG]({d}/rendered/{x["svg"]["file"]})','']
  lines+=['<details>','<summary>查看初稿实际画面</summary>','']
  for x in r['stages'][0]['render']:
   for file in x.get('svg_images',[x['png']['file']]):lines += [f'![初稿 {names[c]}]({d}/rendered/{file})','']
  lines+=['</details>','']
lines+=['## 证据与限制','', '四条轨迹独立容器、独立会话、无其他组输出挂载；各阶段实际模型与源码哈希见 [runs.json](runs.json)。生成不调用工具，渲染由控制器完成，不测客户端自动加载。每题每组一个样本，主 Agent 知道组别后评审；不能据此宣布普遍排名。','', '[内容评审](content-review.json) · [用量与修订规模](metrics.json) · [Mermaid 语法检查](syntax-results.json) · [输入及输出完整性](integrity-results.json)','', '本轮没有测试 am、diagram-design 或 mermaid-diagrams 的原生接入；不用未加载的工具为输出背书。渲染成功不是语义或理解效果证明；具体问题以原始材料、源码与实际画面为依据。','']
(B/'comparison.md').write_text('\n'.join(lines))
