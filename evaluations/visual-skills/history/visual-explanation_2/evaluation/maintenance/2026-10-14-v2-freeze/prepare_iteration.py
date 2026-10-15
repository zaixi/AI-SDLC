#!/usr/bin/env python3
"""Prepare one fresh evaluation suite without running tools or model requests."""
import argparse
import datetime
import hashlib
import json
from pathlib import Path
import shutil

HERE = Path(__file__).resolve().parent
BASE = HERE.parents[1]
TEMPLATE = BASE / '2026-10-14-grok47-failed-retry-2'
CASES = BASE / '2026-10-14-grok47-simplified-once'


def read(path):
    return json.loads(path.read_text())


def write(path, value):
    path.write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def digest(path):
    return hashlib.sha256(path.read_bytes()).hexdigest()


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--output', required=True, type=Path, help='New directory; must not exist')
    parser.add_argument('--skill-dir', type=Path, default=HERE / 'snapshot/visual-explanation_2')
    parser.add_argument('--cases', default='all', help='all or comma-separated original case IDs')
    args = parser.parse_args()
    output = args.output.expanduser().resolve()
    skill = args.skill_dir.expanduser().resolve()
    if output.exists():
        parser.error('Output already exists; preserve historical runs and choose a new directory')
    if not (skill / 'SKILL.md').is_file():
        parser.error('Missing SKILL.md in skill directory')
    if (skill / 'references').exists() or (skill / 'scripts').exists() or (skill / 'assets').exists():
        parser.error('This preparer supports the current self-contained skill; review the generation allowlist before testing added resources')
    cases = read(CASES / 'inputs/cases.json')
    selected = None if args.cases == 'all' else set(args.cases.split(','))
    known = {c['id'] for c in cases['cases']}
    if selected is not None and (not selected or selected - known):
        parser.error('Unknown case IDs: ' + ', '.join(sorted((selected or set()) - known)))
    cases['cases'] = [c for c in cases['cases'] if selected is None or c['id'] in selected]
    cases['status'] = 'prepared_not_run'
    scripts = [p for p in (TEMPLATE / 'scripts').iterdir()
               if p.is_file() and p.name not in ('consolidate.py', 'blind_review.py')]
    source_manifest = read(TEMPLATE / 'manifest.json')
    protocol = read(TEMPLATE / 'protocol.json')
    output.mkdir(parents=True)
    for name in ['scripts', 'preflight', 'runs']:
        (output / name).mkdir()
    for name in ['dependencies', 'judge']:
        shutil.copytree(TEMPLATE / name, output / name)
    shutil.copytree(CASES / 'inputs', output / 'inputs')
    for script in scripts:
        shutil.copy2(script, output / 'scripts' / script.name)
    for name in ['SKILL.md', 'LICENSE.show-me', 'agents/openai.yaml']:
        source = skill / name
        if source.exists():
            target = output / 'snapshots/visual-explanation' / name
            target.parent.mkdir(parents=True, exist_ok=True)
            shutil.copy2(source, target)
    shutil.copy2(HERE / 'RUBRIC.md', output / 'judge/rubric.md')
    write(output / 'inputs/cases.json', cases)
    now = datetime.datetime.now(datetime.timezone.utc).isoformat()
    manifest = {k: source_manifest[k] for k in
                ['conditions', 'generation_skill_allowlist', 'generation_specialist_allowlist']}
    manifest.update(suite_id=output.name, created_at_utc=now, status='prepared_not_run',
                    case_count=len(cases['cases']), planned_repeats=1, planned_outputs=len(cases['cases']),
                    skill_source=str(skill), harness_source=str(TEMPLATE), cases_source=str(CASES),
                    condition_note='visual-explanation is a legacy harness slot; identify actual skill by snapshot name and hashes',
                    snapshot_hashes={'visual-explanation': {
                        str(p.relative_to(output / 'snapshots/visual-explanation')): digest(p)
                        for p in sorted((output / 'snapshots/visual-explanation').rglob('*')) if p.is_file()}},
                    files={str(p.relative_to(output)): digest(p) for folder in ['scripts', 'inputs', 'judge']
                           for p in sorted((output / folder).rglob('*')) if p.is_file()},
                    dependency_manifest_sha256=digest(output / 'dependencies/manifest.json'))
    write(output / 'manifest.json', manifest)
    for key in ['actual_generation_requests', 'requests_without_complete_usage', 'early_termination',
                'client_http_retries', 'review_browser_checks', 'verified_wire_reasoning_effort',
                'review_model_requests']:
        protocol.pop(key, None)
    protocol.update(frozen_at_utc=now, cases=len(cases['cases']), planned_outputs=len(cases['cases']),
                    protocol_revision=2, purpose='Prepared next iteration; no generation has run',
                    parent_protocol=str(TEMPLATE / 'protocol.json'),
                    changes_from_parent=['New selected cases and skill snapshot', 'Understanding-focused evaluator rubric'],
                    retry_policy='One attempt per case; any additional case attempt is separately authorized and recorded; client HTTP retries may occur',
                    review_policy='Use judge/rubric.md; manual artifact review by default; no independent judge calls implied',
                    review_overlapped_generation=False,
                    reasoning='Configured high; verify actual new wire requests before reporting',
                    scripts_sha256={p.name: digest(p) for p in (output / 'scripts').iterdir()})
    write(output / 'protocol.json', protocol)
    (output / 'plan.md').write_text(
        '# 待执行测试\n\n每题一次；当前只准备目录，未调用模型。\n\n'
        '执行前填写：本轮假设、与冻结版的差异、为什么选择这些题、比较条件。\n'
        f'\n测试方法：{HERE / "TESTING.md"}\n'
        '生成阶段不挂载本文件、judge 或历史结论。条件名 visual-explanation 是旧 harness 槽位，实际版本以 snapshots 和 manifest 为准。\n')
    print(json.dumps({'prepared': str(output), 'cases': [c['id'] for c in cases['cases']],
                      'model_calls': 0, 'next': 'Fill plan.md; follow TESTING.md before running'}, ensure_ascii=False))


if __name__ == '__main__':
    main()
