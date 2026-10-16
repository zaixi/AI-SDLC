"""Summarize completed attempts, including truncation and actual skill reads."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
rows = []
for path in sorted((ROOT / 'runs').glob('*/result.json')):
    result = json.loads(path.read_text())
    run = path.parent
    usages = [json.loads(p.read_text()) for p in sorted(run.glob('usage-*.json'))]
    row = {k: result[k] for k in ['id', 'case', 'condition', 'exit', 'seconds', 'model_requests', 'output_tokens', 'budget_exhausted']}
    row['input_tokens'] = sum(u['usage'].get('prompt_tokens', 0) for u in usages)
    row['finish_reasons'] = [f for u in usages for f in u.get('finish_reasons', [])]
    row['reasoning_tokens'] = sum(u['usage'].get('completion_tokens_details', {}).get('reasoning_tokens', 0) for u in usages)
    row['output_cap_reached'] = row['output_tokens'] >= 49152
    row['upstream_errors'] = len(list(run.glob('upstream-error-*.json')))
    row['reads'] = []
    row['tool_failures'] = []
    for line in (run / 'events.jsonl').read_text().splitlines():
        event = json.loads(line)
        part = event.get('part', {})
        state = part.get('state', {})
        if part.get('tool') == 'read' and state.get('status') == 'completed':
            row['reads'].append(state.get('input', {}).get('filePath'))
        if state.get('status') == 'error':
            row['tool_failures'].append({'tool': part.get('tool'), 'input': state.get('input'), 'error': state.get('error')})
    row['reads'] = sorted(set(x for x in row['reads'] if x))
    row['artifacts'] = [{'path': str(p.relative_to(run / 'work')), 'bytes': p.stat().st_size} for p in sorted((run / 'work').rglob('*')) if p.is_file() and '__pycache__' not in p.parts]
    rows.append(row)
(ROOT / 'review/metrics.json').write_text(json.dumps(rows, ensure_ascii=False, indent=2))
for row in rows:
    print(json.dumps({k: row[k] for k in ['id', 'exit', 'seconds', 'model_requests', 'output_tokens', 'input_tokens', 'finish_reasons']}, ensure_ascii=False))
