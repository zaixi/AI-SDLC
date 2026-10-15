"""Audit frozen inputs, completed sessions, and actual extension tool calls."""
import hashlib
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def write(name, data):
    (ROOT / 'review' / name).write_text(json.dumps(data, ensure_ascii=False, indent=2) + '\n')


def main():
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    snapshot = ROOT / 'snapshots/visual-explanation'
    installed = Path('/home/liyujiang/.codex/skills/visual-explanation')
    hashes = manifest['snapshot_hashes']['visual-explanation']
    snapshot_ok = all(digest(snapshot / name) == value for name, value in hashes.items())
    installed_ok = all((installed / name).exists() and digest(installed / name) == value for name, value in hashes.items())
    execution, backends, recovered = [], [], []
    from prepare_review import delivered_answer
    for directory in sorted((ROOT / 'runs').iterdir()):
        result = json.loads((directory / 'result.json').read_text())
        events = [json.loads(line) for line in (directory / 'events.jsonl').read_text().splitlines() if line.startswith('{')]
        seen, calls = set(), []
        for event in events:
            if event.get('type') == 'tool_use':
                part = event['part']
                if part.get('callID') not in seen:
                    calls.append(part)
                    seen.add(part.get('callID'))
        reads, renders, semantic_reads = set(), [], 0
        for call in calls:
            state = call.get('state', {})
            args = json.dumps(state.get('input', {}), ensure_ascii=False)
            for name in manifest['generation_specialist_allowlist']['visual-explanation']:
                if '/input/specialists/' + name in args and 'SKILL.md' in args:
                    reads.add(name)
            semantic_reads += 'references/semantics.md' in args
            command = state.get('input', {}).get('command', '')
            if call.get('tool') == 'bash' and re.search(r'am\.mjs[\"\x27]?\s+render\b', command):
                output = str(state.get('output', ''))
                renders.append({'call_id': call.get('callID'), 'command': command,
                                'status': state.get('status'), 'output': output[:1200]})
        backends.append({'case': result['case'], 'run': result['id'], 'specialist_reads': sorted(reads),
                         'semantics_read_calls': semantic_reads, 'render_calls': len(renders), 'renders': renders})
        fs = json.loads((directory / 'filesystem-audit.json').read_text())
        frozen_inputs_match = all(digest(directory / 'input/skill' / name) == hashes[name]
                                  for name in manifest['generation_skill_allowlist']['visual-explanation'])
        requests = [json.loads(f.read_text()) for f in sorted(directory.glob('request-*.json'))]
        generation_requests = [r for r in requests if r.get('tools')]
        execution.append({'case': result['case'], 'exit': result['exit'], 'frozen_inputs_match': frozen_inputs_match,
                          'filesystem_audit': fs, 'models': sorted(set(r['model'] for r in generation_requests)),
                          'max_output_limits': sorted(set(r.get('max_tokens', r.get('max_completion_tokens')) for r in generation_requests)),
                          'api_errors': len(list(directory.glob('upstream-error-*.json'))),
                          'budget_exhausted': result['budget_exhausted']})
        answer, note = delivered_answer(directory)
        if note != 'final_stop_message' or not answer.strip():
            recovered.append({'case': result['case'], 'note': note, 'recovered_answer_nonempty': bool(answer.strip())})
    write('backend-audit.json', backends)
    write('execution-audit.json', {'snapshot_matches_manifest': snapshot_ok, 'installed_skill_unchanged': installed_ok,
                                 'completed_sessions': len(execution), 'sessions': execution})
    write('cli-log-anomaly.json', recovered)
    print(json.dumps({'completed_sessions': len(execution), 'snapshot_ok': snapshot_ok, 'installed_unchanged': installed_ok,
                      'render_cases': [x['case'] for x in backends if x['render_calls']], 'recovered_replies': len(recovered)}))


if __name__ == '__main__':
    main()
