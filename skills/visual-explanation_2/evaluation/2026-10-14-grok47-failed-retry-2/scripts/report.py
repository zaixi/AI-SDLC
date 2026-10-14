"""Aggregate quality, coverage, paired preferences, and full generation costs."""
from pathlib import Path
import collections
import html
import json
import re
import statistics
import run
from prepare_review import delivered_answer

ROOT = run.ROOT
REVIEW = ROOT / 'review'
WEIGHTS = {'semantic': 45, 'fit': 20, 'readability': 20, 'delivery': 15}


def mean(values):
    return round(statistics.mean(values), 2) if values else None


def metrics(directory):
    usage = []
    for path in directory.glob('usage-*.json'):
        item = json.loads(path.read_text())['usage']
        if item:
            usage.append(item)
    tools = []
    seen = set()
    for line in (directory / 'events.jsonl').read_text().splitlines():
        try:
            event = json.loads(line)
        except ValueError:
            continue
        if event.get('type') == 'tool_use':
            part = event['part']
            if part.get('callID') not in seen:
                tools.append(part)
                seen.add(part.get('callID'))
    input_total = sum(x.get('prompt_tokens', 0) for x in usage)
    output_total = sum(x.get('completion_tokens', 0) for x in usage)
    reasoning = sum(x.get('completion_tokens_details', {}).get('reasoning_tokens', 0) for x in usage)
    reasoning_records = sum('reasoning_tokens' in x.get('completion_tokens_details', {}) for x in usage)
    cache_records = [x['prompt_tokens_details']['cached_tokens'] for x in usage if 'cached_tokens' in x.get('prompt_tokens_details', {})]
    specialist = {}
    for name in ['mermaid-diagrams', 'diagram-design', 'answer-me-with-html']:
        read_count = 0
        backend_count = 0
        render_count = 0
        for tool in tools:
            args = json.dumps(tool.get('state', {}).get('input', {}), ensure_ascii=False)
            if '/input/specialists/' + name in args:
                if 'SKILL.md' in args:
                    read_count += 1
                if tool['tool'] == 'bash' and 'am.mjs' in args:
                    backend_count += 1
                    command = tool.get('state', {}).get('input', {}).get('command', '')
                    render_count += bool(re.search(r'am\.mjs[\"\x27]?\s+render\b', command))
        specialist[name] = {'skill_read_calls': read_count, 'backend_command_calls': backend_count, 'backend_render_calls': render_count}
    references = sum('/references/' in json.dumps(t.get('state', {}).get('input', {})) for t in tools)
    return {'input_tokens': input_total, 'output_tokens_including_reasoning': output_total, 'reported_reasoning_tokens': reasoning if reasoning_records else None,
            'reasoning_usage_records': reasoning_records, 'reported_cache_read_tokens': sum(cache_records) if cache_records else None, 'cache_usage_records': len(cache_records),
            'usage_records': len(usage), 'tool_calls': len(tools), 'reference_path_tool_calls': references,
            'write_edit_calls': sum(t['tool'] in ('write', 'edit') for t in tools), 'specialists': specialist}


def main():
    mapping = json.loads((REVIEW / 'private-mapping.json').read_text())
    adjudication_path = REVIEW / 'adjudication.json'
    adjudication = json.loads(adjudication_path.read_text()) if adjudication_path.exists() else {}
    audit_notes = {**adjudication.get('rejected_critical_verdicts', {}), **adjudication.get('rejected_other_deductions', {}), **adjudication.get('supplementary_missing_score_checks', {}), **adjudication.get('missed_factual_errors', {})}
    rows = []
    validation = []
    for item in mapping:
        directory = ROOT / 'runs' / item['run']
        result = json.loads((directory / 'result.json').read_text())
        (directory / 'final-answer.md').write_text(delivered_answer(directory)[0] + '\n')
        score_path = REVIEW / 'scores' / item['sample'] / 'result.json'
        score = json.loads(score_path.read_text()) if score_path.exists() else None
        total = None
        if score and score.get('scores') is not None:
            scores = score['scores']
            valid = set(scores) == set(WEIGHTS) and all(type(v) is int and 0 <= v <= 4 for v in scores.values())
            valid = valid and all(type(score.get(k)) is bool for k in ['semantic_pass', 'delivery_pass', 'qualified'])
            valid = valid and score.get('qualified') == (score.get('semantic_pass') and score.get('delivery_pass'))
            if score.get('critical_errors') and scores.get('semantic', 9) > 1:
                valid = False
            if score.get('critical_errors') and score.get('semantic_pass'):
                valid = False
            if not valid:
                validation.append({'sample': item['sample'], 'problem': 'Scoring schema or rubric invariant mismatch'})
            else:
                total = sum(scores[k] / 4 * weight for k, weight in WEIGHTS.items())
        rows.append({'sample': item['sample'], 'run': item['run'], 'condition': result['condition'], 'case': result['case'], 'group': result['group'],
                     'repeat': result['repeat'], 'seconds': result['seconds'], 'model_requests': result['model_requests'], 'exit': result['exit'],
                     'generation_errors': bool(result['errors']), 'budget_exhausted': result['budget_exhausted'], 'total': total, 'score': score, **metrics(directory)})
        rows[-1]['requests_without_usage'] = result['model_requests'] - rows[-1]['usage_records']
        rows[-1]['upstream_http_error_records'] = len(list(directory.glob('upstream-error-*.json')))
    summary = {}
    for condition in run.CONDITIONS:
        selected = [r for r in rows if r['condition'] == condition]
        scored = [r for r in selected if r['total'] is not None]
        case_averages = {case: statistics.mean(values) if (values := [r['total'] for r in scored if r['case'] == case]) else None for case in sorted({r['case'] for r in selected})}
        group_averages = {g: statistics.mean(values) if (values := [v for case, v in case_averages.items() if case.startswith(g) and v is not None]) else None for g in 'ABCD'}
        case_means = {case: round(value, 2) if value is not None else None for case, value in case_averages.items()}
        groups = {g: round(value, 2) if value is not None else None for g, value in group_averages.items()}
        summary[condition] = {'samples': len(selected), 'scored': len(scored), 'coverage': round(len(scored) / len(selected), 4) if selected else None,
                              'quality': mean([v for v in group_averages.values() if v is not None]), 'groups': groups, 'case_means': case_means,
                              'semantic_pass': sum(r['score']['semantic_pass'] for r in scored), 'delivery_pass': sum(r['score']['delivery_pass'] for r in scored),
                              'qualified': sum(r['score']['qualified'] for r in scored), 'mean_seconds': mean([r['seconds'] for r in selected]),
                              'median_seconds': statistics.median([r['seconds'] for r in selected]) if selected else None,
                              'input_tokens': sum(r['input_tokens'] for r in selected), 'output_tokens_including_reasoning': sum(r['output_tokens_including_reasoning'] for r in selected),
                              'model_requests': sum(r['model_requests'] for r in selected), 'tool_calls': sum(r['tool_calls'] for r in selected),
                              'requests_without_usage': sum(r['requests_without_usage'] for r in selected),
                              'specialist_samples': {name: sum(r['specialists'][name]['skill_read_calls'] > 0 for r in selected) for name in ['mermaid-diagrams', 'diagram-design', 'answer-me-with-html']},
                              'backend_samples': sum(r['specialists']['answer-me-with-html']['backend_command_calls'] > 0 for r in selected),
                              'backend_render_samples': sum(r['specialists']['answer-me-with-html']['backend_render_calls'] > 0 for r in selected),
                              'dimensions': {k: mean([r['score']['scores'][k] for r in scored]) for k in WEIGHTS},
                              'timeouts': sum(r['exit'] == 'timeout' for r in selected),
                              'budget_exhaustions': sum(r['budget_exhausted'] for r in selected),
                              'upstream_http_error_records': sum(r['upstream_http_error_records'] for r in selected)}
    pairs = collections.defaultdict(lambda: {'left_wins': 0, 'right_wins': 0, 'ties': 0, 'unavailable': 0})
    row_by_sample = {r['sample']: r for r in rows}
    pair_map = REVIEW / 'private-pair-mapping.json'
    if pair_map.exists():
        for job in json.loads(pair_map.read_text()):
            conditions = sorted([row_by_sample[job['left']]['condition'], row_by_sample[job['right']]['condition']])
            key = ' vs '.join(conditions)
            path = REVIEW / 'pairs' / job['id'] / 'result.json'
            value = json.loads(path.read_text()) if path.exists() else {}
            winner = value.get('winner')
            if winner == 'tie':
                pairs[key]['ties'] += 1
            elif winner in ('left', 'right'):
                winning_condition = row_by_sample[job[winner]]['condition']
                pairs[key]['left_wins' if winning_condition == conditions[0] else 'right_wins'] += 1
            else:
                pairs[key]['unavailable'] += 1
    run.write_json(REVIEW / 'summary.json', {'conditions': summary, 'pairs': dict(pairs), 'validation_issues': validation})
    run.write_json(REVIEW / 'sample-metrics.json', rows)
    sections = []
    for case in json.loads((ROOT / 'inputs/cases.json').read_text())['cases']:
        cards = []
        for row in sorted([r for r in rows if r['case'] == case['id']], key=lambda r: (r['repeat'], r['condition'])):
            package = REVIEW / 'anonymous' / row['sample']
            evidence = json.loads((package / 'evidence.json').read_text())
            reply_label = '原始最终回复' if evidence['reply_scope'] == 'final_stop_message' else '服务端最终回复（CLI 日志缺失）' if evidence['reply_scope'] == 'provider_stream_recovered_cli_text_missing' else '中断前消息（无最终回复）'
            links = [f'<a href="runs/{row["run"]}/final-answer.md">{reply_label}</a>', f'<a href="review/anonymous/{row["sample"]}/answer.md">匿名评审文本</a>']
            if row['score']:
                links.append(f'<a href="review/scores/{row["sample"]}/result.json">原始评分依据</a>')
            pictures = []
            for artifact in evidence['artifacts']:
                links.append(f'<a href="review/anonymous/{row["sample"]}/{artifact["source"]}">{html.escape(artifact["source"])}</a>')
                for render in artifact['renders']:
                    if render['width'] == 390 and render.get('screenshot'):
                        links.append(f'<a href="review/anonymous/{row["sample"]}/{render["screenshot"]}">手机预览（{html.escape(artifact["source"]) }）</a>')
                    if (render['width'] == 1280 or render.get('native_png')) and render.get('screenshot'):
                        src = f'review/anonymous/{row["sample"]}/{render["screenshot"]}'
                        pictures.append(f'<a href="{src}"><img loading="lazy" src="{src}"></a>')
            answer = html.escape((package / 'answer.md').read_text())
            if row['sample'] in audit_notes:
                links.append('<strong>' + html.escape(audit_notes[row['sample']]['note']) + '</strong>')
            cards.append(f'<article><h3>{html.escape(row["condition"])} · 第 {row["repeat"]} 次</h3><p>Grok 4.7 high · {"超时，以下文件未完成最终交付" if row["exit"] == "timeout" else "流结束异常，无最终交付" if evidence["reply_scope"] == "partial_visible_messages_no_final_stop" else "服务端完成；CLI 末条日志缺失" if evidence["reply_scope"] == "provider_stream_recovered_cli_text_missing" else "正常交付"} · {row["seconds"]} s</p><p>{" · ".join(links)}</p>{"".join(pictures)}<details><summary>回复原文</summary><pre>{answer}</pre></details></article>')
        sections.append(f'<section id="{case["id"]}"><h2>{case["id"]} {html.escape(case["title"])}</h2><p>{html.escape(case["prompt"])}</p><div class="grid">{"".join(cards)}</div></section>')
    page = '<!doctype html><html lang="zh-CN"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>Grok 4.7 · visual-explanation · 单次评测</title><style>body{font:16px/1.6 system-ui,sans-serif;margin:32px;background:#f6f7f8;color:#202832}main{max-width:1500px;margin:auto}h1,h2,h3{line-height:1.3}.grid{display:grid;grid-template-columns:1fr;gap:16px}article{background:white;padding:18px;border:1px solid #dce1e6;border-radius:8px;min-width:0}img{width:100%;height:230px;object-fit:contain;object-position:top}pre{white-space:pre-wrap;overflow-wrap:anywhere;font-size:13px}section{margin:42px 0}a{color:#14589d}@media(max-width:850px){body{margin:16px}.grid{grid-template-columns:1fr}}</style><main><h1>Grok 4.7 · visual-explanation · 单次评测</h1><p>原题、原始回复和实际渲染。成本与质量分开呈现；本轮不做模型数值评分；逐题复核并非盲评。每题只生成一次，超时不补跑。</p>' + ''.join(sections) + '</main></html>'
    navigation = '<p><a href="report.md">完整结论与逐题复核</a> · <a href="review/summary.json">原始汇总数据</a></p><nav>' + ' · '.join(f'<a href="#{case["id"]}">{case["id"]}</a>' for case in json.loads((ROOT / 'inputs/cases.json').read_text())['cases']) + '</nav>'
    page = page.replace('<section id=', navigation + '<section id=', 1)
    (ROOT / 'gallery.html').write_text(page)
    print(json.dumps({'samples': len(rows), 'scored': sum(r['total'] is not None for r in rows), 'validation_issues': validation, 'conditions': summary}, ensure_ascii=False, indent=2))


if __name__ == '__main__':
    main()
