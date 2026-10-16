"""Summarize verified runs without treating exit zero as task completion."""
from pathlib import Path
import json

ROOT = Path(__file__).resolve().parents[1]
records = json.loads((ROOT / 'review/results.json').read_text())
for record in records:
    run = ROOT / 'runs' / record['id']
    usage = [json.loads(p.read_text()) for p in sorted(run.glob('usage-*.json'))]
    record['finish_reasons'] = [x for u in usage for x in u.get('finish_reasons', [])]
    record['truncated'] = 'length' in record['finish_reasons']
    record['reasoning_tokens'] = sum(u.get('usage', {}).get('completion_tokens_details', {}).get('reasoning_tokens', 0) for u in usage)
    reads = []
    for line in (run / 'events.jsonl').read_text().splitlines():
        event = json.loads(line)
        part = event.get('part', {})
        state = part.get('state', {})
        if part.get('tool') == 'read' and state.get('status') == 'completed':
            reads.append(state.get('input', {}).get('filePath'))
        if part.get('tool') == 'bash' and state.get('status') == 'completed':
            command = state.get('input', {}).get('command', '')
            output = state.get('output', '')
            for source in (run / 'input').rglob('*.md'):
                path = '/input/' + str(source.relative_to(run / 'input'))
                if ('cat ' + path) in command and source.read_text() in output:
                    reads.append(path)
    record['instruction_reads'] = sorted(set(p for p in reads if p and p.startswith('/input/')))
    record['sizes'] = {}
    for category in ['production', 'tests', 'docs']:
        files = []
        for path in (run / 'work').rglob('*'):
            if not path.is_file() or '__pycache__' in path.parts:
                continue
            relative = path.relative_to(run / 'work')
            kind = 'tests' if 'tests' in relative.parts else 'production' if path.suffix == '.py' else 'docs' if path.suffix == '.md' else None
            if kind == category:
                files.append(path)
        record['sizes'][category] = {
            'files': len(files),
            'lines': sum(len(p.read_text().splitlines()) for p in files),
            'nonblank_lines': sum(sum(bool(s.strip()) for s in p.read_text().splitlines()) for p in files),
            'bytes': sum(p.stat().st_size for p in files),
        }
    record['passes_frozen_checks'] = all(c['exit'] == 0 for c in record['checks'])
    record['delivered'] = record['exit'] == 0 and not record['truncated'] and bool(record['changes'])
    print(json.dumps({k: record[k] for k in ['id', 'delivered', 'passes_frozen_checks', 'truncated', 'output_tokens', 'seconds', 'sizes', 'instruction_reads']}, ensure_ascii=False))
(ROOT / 'review/metrics.json').write_text(json.dumps(records, ensure_ascii=False, indent=2))
