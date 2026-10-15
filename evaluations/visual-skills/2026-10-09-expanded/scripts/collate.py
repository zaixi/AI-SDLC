"""Collate unchanged answers; fail on missing answers or changed inputs."""
import hashlib
import json
import re
import sys
from pathlib import Path

base = Path(sys.argv[1]).resolve()
protocol = json.loads((base / 'protocol.json').read_text())
prompts = json.loads((base / 'inputs/prompts.json').read_text())
conditions = protocol['conditions']
runs = ['outputs', 'repeat-outputs']

for item in json.loads((base / 'input-manifest.json').read_text()):
    assert hashlib.sha256((base / item['file']).read_bytes()).hexdigest() == item['sha256'], item['file']

records = []
for run in runs:
    for condition in conditions:
        directory = base / run / condition
        provenance = json.loads((directory / 'provenance.json').read_text())
        allowed = str(base / 'inputs' / condition) + '/'
        common = str(base / 'inputs/prompts.json')
        for source in provenance['read_files']:
            assert source == common or source.startswith(allowed), (directory, source)
        for case in prompts:
            path = directory / (case + '.md')
            raw = path.read_bytes()
            body = raw.decode('utf-8')
            assert body.strip(), path
            mermaid = re.findall(r'```mermaid\s*\n([\s\S]*?)```', body)
            records.append({
                'file': str(path.relative_to(base)), 'run': run,
                'condition': condition, 'case': case,
                'sha256': hashlib.sha256(raw).hexdigest(), 'characters': len(body),
                'mermaid_blocks': len(mermaid),
                'diagram_types': [m.strip().splitlines()[0] for m in mermaid],
                'has_diff': bool(re.search(r'```diff\s*\n', body)),
            })

def comparison(run, cases, filename, title):
    sections = ['# ' + title, '\n逐字汇集未改写的原始文件；语法解析与事实审阅见 [主报告](README.md)。显示效果取决于阅读平台，本轮未验证布局。\n']
    for case in cases:
        sections += ['## ' + case, '\n' + prompts[case] + '\n']
        for condition in conditions:
            path = Path(run) / condition / (case + '.md')
            sections += ['### ' + condition, '\n[原文件](' + str(path) + ')\n', (base / path).read_text() + '\n']
    (base / filename).write_text('\n'.join(sections))

comparison('outputs', prompts, 'comparison.md', '第一轮：十题、五组独立生成对照')
comparison('repeat-outputs', prompts, 'repeat-comparison.md', '第二轮：十题、五组独立生成对照')
comparison('outputs', [c for c in prompts if c[:2] in ['07', '08', '09', '10']], 'new-cases-comparison.md', '新增四题：第一轮五组独立生成对照')
(base / 'raw-output-manifest.json').write_text(json.dumps(records, ensure_ascii=False, indent=2) + '\n')
summary = []
for condition in conditions:
    items = [r for r in records if r['condition'] == condition]
    summary.append({'condition': condition, 'answers': len(items),
                    'average_characters': round(sum(r['characters'] for r in items) / len(items), 1),
                    'mermaid_blocks': sum(r['mermaid_blocks'] for r in items),
                    'diff_answers': sum(r['has_diff'] for r in items),
                    'characters_by_case': {c: [r['characters'] for r in items if r['case'] == c] for c in prompts}})
(base / 'metrics.json').write_text(json.dumps(summary, ensure_ascii=False, indent=2) + '\n')
print(json.dumps({'answers': len(records), 'conditions': summary}, ensure_ascii=False, indent=2))
