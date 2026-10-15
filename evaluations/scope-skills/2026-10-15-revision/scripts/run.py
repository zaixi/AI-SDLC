"""Fresh three-condition comparison, reusing the frozen request executor."""
from concurrent.futures import ThreadPoolExecutor, as_completed
from datetime import datetime, timezone
from pathlib import Path
import importlib.util
import json
import random

ROOT = Path(__file__).resolve().parents[1]
PARENT = ROOT.with_name('2026-10-15-design')
spec = importlib.util.spec_from_file_location('scope_executor', PARENT / 'scripts/run.py')
core = importlib.util.module_from_spec(spec)
spec.loader.exec_module(core)


def main():
    if (ROOT / 'protocol.json').exists():
        raise RuntimeError('Refusing to overwrite a frozen evaluation')
    raw = Path('/home/liyujiang/.codex/skill-evaluations/scope/2026-10-15-revision')
    cases = {c['id']: c for c in json.loads((ROOT / 'inputs/cases.json').read_text())['cases']}
    parent = json.loads((PARENT / 'protocol.json').read_text())
    assert core.sha((PARENT / 'scripts/run.py').read_bytes()) == parent['frozen_hashes']['scripts/run.py']
    conditions = ['original', 'revised', 'original-plus-boring']
    sources = {}
    for condition in conditions:
        base = raw / 'snapshots' / condition
        files = [base / 'AGENTS.md'] + sorted(p for p in base.rglob('*.md') if p != base / 'AGENTS.md')
        sources[condition] = {'files': [{'path': str(p.relative_to(base)), 'sha256': core.sha(p.read_bytes())} for p in files]}
    jobs = []
    for case in cases:
        order = conditions.copy()
        random.Random('scope-revision-' + case).shuffle(order)
        jobs.extend({'id': case + '-' + c, 'case': case, 'condition': c} for c in order)
    protocol = {k: parent[k] for k in ['model', 'reasoning_effort', 'max_tokens', 'concurrency', 'request_timeout_seconds', 'stream_wall_limit_seconds', 'temperature', 'seed']}
    protocol.update(created_utc=datetime.now(timezone.utc).isoformat(), raw_root=str(raw),
                    sources=sources, jobs=jobs, repeats=1,
                    activation='Same user-message skill-file wrapper for all groups; full AGENTS text; no native Codex loading',
                    comparison='All 15 cells freshly generated, old D01-D03 plus two new synthetic held-out cases D04-D05; original-plus-boring uses original AGENTS, not revised',
                    review='Fixed rubric, manual nonblind, no feedback or retries; all reference files supplied upfront; no tools or other host instructions',
                    boring_source=parent['sources']['boring-engineering'],
                    frozen_hashes={p: core.sha((ROOT / p).read_bytes()) for p in ['inputs/cases.json', 'RUBRIC.md', 'scripts/run.py', '../2026-10-15-design/scripts/run.py']})
    core.save(ROOT / 'protocol.json', protocol)
    core.save(raw / 'protocol.json', protocol)
    opts = core.provider()
    with ThreadPoolExecutor(max_workers=protocol['concurrency']) as pool:
        futures = [pool.submit(core.execute, job, protocol, opts, cases) for job in jobs]
        results = [f.result() for f in as_completed(futures)]
    core.save(raw / 'results.json', sorted(results, key=lambda r: r['id']))


if __name__ == '__main__':
    main()
