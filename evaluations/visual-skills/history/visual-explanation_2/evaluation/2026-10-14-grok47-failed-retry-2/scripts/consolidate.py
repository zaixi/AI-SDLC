"""Summarize all attempts of the same frozen skill; never select the best output."""
from pathlib import Path
import html
import json
import os
import collections

ROOT = Path(__file__).resolve().parents[1]
BASE = ROOT.parent
SUITES = [BASE / '2026-10-14-grok47-simplified-once',
          BASE / '2026-10-14-grok47-timeout-retry', ROOT]


def read(path):
    return json.loads(path.read_text())


def link(path):
    return os.path.relpath(path, ROOT)


def delivery(result, evidence, upstream_error=False):
    scope = evidence['reply_scope']
    if scope == 'final_stop_message':
        return '正常完成'
    if scope == 'provider_stream_recovered_cli_text_missing':
        return '服务端完成，CLI 漏记'
    if result['exit'] == 'timeout':
        return '超时，有残稿' if evidence['artifacts'] else '超时，无产出'
    return '服务异常，未完成' if upstream_error or result.get('errors') or evidence.get('infrastructure_failure') else '未完成'


def main():
    cases = read(SUITES[0] / 'inputs/cases.json')['cases']
    histories = collections.defaultdict(list)
    totals = []
    notes = {}
    for number, suite in enumerate(SUITES, 1):
        notes.update(read(suite / 'review/manual-case-notes.json'))
        metrics = {r['case']: r for r in read(suite / 'review/sample-metrics.json')}
        suite_total = {'round': number, 'cases': len(metrics)}
        for key in ['input_tokens', 'output_tokens_including_reasoning', 'model_requests', 'tool_calls', 'requests_without_usage']:
            suite_total[key] = sum(r[key] for r in metrics.values())
        totals.append(suite_total)
        for mapping in read(suite / 'review/private-mapping.json'):
            directory = suite / 'runs' / mapping['run']
            result = read(directory / 'result.json')
            package = suite / 'review/anonymous' / mapping['sample']
            evidence = read(package / 'evidence.json')
            histories[result['case']].append({
                'round': number, 'suite': str(suite), 'directory': str(directory),
                'package': str(package), 'status': delivery(result, evidence, bool(list(directory.glob('upstream-error-*.json')))),
                'seconds': result['seconds'], 'metrics': metrics[result['case']],
                'evidence': evidence,
            })
    rows = []
    for case in cases:
        history = histories[case['id']]
        rows.append({'case': case['id'], 'title': case['title'], 'prompt': case['prompt'],
                     'attempts': history, 'latest_status': history[-1]['status'],
                     'quality': notes[case['id']]})
    counts = collections.Counter(r['latest_status'] for r in rows)
    data = {'selection': 'latest attempt per case; original failures preserved; no best-of selection',
            'scope': 'Current frozen skill only; 16 initial cases, 5 first retries, 3 second retries',
            'latest_delivery_counts': dict(counts), 'round_totals': totals, 'cases': rows}
    (ROOT / 'all-cases.json').write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')
    md = ['# visual-explanation：全部 16 个 case 汇总', '',
          '范围：同一冻结版本，OpenCode 1.14.28 + Grok 4.7 high。首轮 16 题、第一次补测 5 题、第二次补测 3 题，共 24 次尝试。每轮每题最多一次；每次 900 秒。未修改 skill、依赖或生成参数。', '',
          '按每题最近一次尝试展示，保留所有历史；不挑选最好结果，不把补测完成率冒充首轮成功率。没有新产物时，质量栏明确回顾历史残稿。完成交付与内容质量分开判断。复核为主代理非盲检查原题、原始输出及适用的浏览器/数值检查，没有独立模型评分。', '',
          '第二次补测三题均在初始请求阶段反复遇到 HTTP 500，约 169 秒后人工终止无效等待，没有执行工具或生成产物。本轮不能用于评价 skill 能力；客户端对同一失败 HTTP 请求的重试不代表重新采样 case。', '',
          '[全部产出画廊](all-cases.html) · [本轮三题画廊](gallery.html)', '',
          '最近一次交付状态：' + '；'.join(f'{k} {v}/16' for k, v in counts.items()) + '。', '',
          '| Case | 主题 | 各次交付状态 / 秒 | 产出质量与历史问题 |',
          '|---|---|---|---|']
    cards = []
    for row in rows:
        case_id = row['case']
        chain = ' → '.join(f'{a["status"]} / {a["seconds"]:.0f}' for a in row['attempts'])
        note = row['quality']['note']
        md.append(f'| [{case_id}](all-cases.html#{case_id}) | {row["title"]} | {chain} | {note.replace("|", " / ")} |')
        attempt_html = []
        for a in row['attempts']:
            directory = Path(a['directory'])
            package = Path(a['package'])
            final = directory / 'final-answer.md'
            if not final.exists():
                final = directory / 'answer.md'
            links = [f'<a href="{html.escape(link(final))}">回复</a>',
                     f'<a href="{html.escape(link(package / "evidence.json"))}">验证证据</a>']
            pictures = []
            for artifact in a['evidence']['artifacts']:
                links.append(f'<a href="{html.escape(link(package / artifact["source"]))}">原始产物 {html.escape(artifact["source"])}</a>')
                for render in artifact['renders']:
                    if render.get('exit') == 0 and render.get('screenshot'):
                        url = html.escape(link(package / render['screenshot']))
                        links.append(f'<a href="{url}">{render["width"]}px 截图</a>')
                        if a is row['attempts'][-1] and render['width'] == 1280:
                            pictures.append(f'<a href="{url}"><img loading="lazy" src="{url}" alt="{case_id} 最近产出桌面截图"></a>')
            attempt_html.append(f'<div class="attempt">第 {a["round"]} 轮 · {html.escape(a["status"])} · {a["seconds"]:.2f}s · {a["metrics"]["model_requests"]} 请求<br>' + ' · '.join(links) + '</div>' + ''.join(pictures))
        latest = Path(row['attempts'][-1]['package']) / 'answer.md'
        text = latest.read_text() if latest.exists() else ''
        cards.append(f'<section id="{case_id}"><h2>{case_id} · {html.escape(row["title"])}</h2><p class="verdict">{html.escape(row["quality"]["status"])}</p><p>{html.escape(note)}</p><details><summary>原题</summary><p>{html.escape(row["prompt"])}</p></details>' + ''.join(attempt_html) + '<details><summary>最近一次回复文本</summary><pre>' + html.escape(text) + '</pre></details></section>')
    md += ['', '## 执行成本', '', '包含失败尝试；输入 token 是逐请求累计，包含重复上下文，不能按唯一文本量理解。输出包含推理 token；usage 不完整时为下界。', '',
           '| 轮次 | 题数 | 请求 | 输入 token | 输出 token（含推理） | usage 不完整请求 |', '|---|---:|---:|---:|---:|---:|']
    for t in totals:
        md.append(f'| {t["round"]} | {t["cases"]} | {t["model_requests"]} | {t["input_tokens"]:,} | {t["output_tokens_including_reasoning"]:,} | {t["requests_without_usage"]} |')
    md += ['', '第三轮 token 记录为 0 表示没有收到 usage，实际消耗未知，不能理解为已确认零消耗。', '',
           '首轮主机资源压力明显，补测记录见各目录 preflight/resource-history.jsonl。耗时包含模型、服务与工具等待；不同轮次不能直接归因为 skill 改进。本汇总不与旧版本、show-me 或无 skill 基线混算。', '',
           '## 综合判断', '',
           '- 首轮正常最终回复 11/16；补测后正常最终回复 12/16，另 D03 有完整页面和服务端最终回复但 CLI 漏记；B03、C01、C04 仍未完成。13/16 是累计覆盖，不是单次成功率，更不是质量合格率。',
           '- 核心正确的 9 题：A01、A02、A03、A04、B04、C02、D01、D02、D04。其中 A02、A04、C02 的重复内容仍可收敛。',
           '- 有局部问题的 2 题：B01 状态数文案错误、C03 手机可读性及比较表述欠佳。',
           '- 有实质问题的 2 题：B02 保存次数错误且分支图不连通；D03 缺少紧凑关系总览、箭头语义依赖补充文字，并添加了原文没有保证的索引可见性结论。',
           '- 尚未完成的 3 题：B03、C01、C04。不能用残稿当作正式交付，也不能把本轮 HTTP 500 算成图解能力失败。',
           '- 简单任务的载体选择基本合理：diff、表格、文字可直接解决；复杂关系、准确数值图和交互页面仍不稳定。图更多、页面更长没有自动带来更好理解。',
           '- 依赖不能单独解释结果：diagram-design 在 B04 有帮助，但 B03/C01 仍未完成；am 产出有规则正确的 B01，也有 B02/D03 的问题；C04 未调用这些后端仍耗时很长。现有数据不足以断言某一依赖或检查规则是唯一原因。',
           '- 当前不宜据此继续增加通用检查条款或重写 skill。先将服务可用性、模型长时间推理、工具耗时和最终图解质量分别记录，再用受控实验检验具体假设。本次没有修改 skill。', '']
    (ROOT / 'all-cases.md').write_text('\n'.join(md))
    document = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>visual-explanation 全部 16 题</title><style>body{font:16px/1.6 system-ui,sans-serif;color:#182533;background:#f3f5f7;max-width:1140px;margin:auto;padding:24px}a{color:#145ca0}nav{display:flex;gap:14px;flex-wrap:wrap}section{background:white;border:1px solid #ccd4dd;border-radius:10px;padding:24px;margin:24px 0;scroll-margin-top:20px}.verdict{font-weight:700}.attempt{padding:10px 0;border-top:1px solid #ddd;margin-top:12px}img{display:block;max-width:100%;max-height:700px;object-fit:contain;object-position:top;margin:14px auto}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:14px}summary{cursor:pointer}h2{font-size:21px}@media(max-width:600px){body{padding:12px}section{padding:16px}}</style><h1>visual-explanation · 全部 16 题</h1><p>同一冻结 skill，OpenCode + Grok 4.7 high。16 + 5 + 3 = 24 次尝试；每次限时 900 秒。按最近一次展示，保留失败历史，不挑最好结果。</p><p>交付完成不代表质量合格。主代理非盲复核，无独立模型评分。</p><p><a href="all-cases.md">完整总结</a> · <a href="report.md">本轮重试报告</a></p><nav>' + ''.join(f'<a href="#{r["case"]}">{r["case"]}</a>' for r in rows) + '</nav>' + ''.join(cards) + '</html>'
    (ROOT / 'all-cases.html').write_text(document)
    print(json.dumps({'cases': len(rows), 'attempts': sum(len(r['attempts']) for r in rows), 'latest_status': counts}, ensure_ascii=False))


if __name__ == '__main__':
    main()
