"""Operate the retry controls in the original artifact, preserving all screenshots."""
from pathlib import Path
import json
import shutil
import prepare_review
import run

ROOT = run.ROOT
CHECK_VERSION = 2


if __name__ == '__main__':
    mapping = json.loads((ROOT / 'review/private-mapping.json').read_text())
    for item in mapping:
        package = ROOT / 'review/anonymous' / item['sample']
        evidence_path = package / 'evidence.json'
        evidence = json.loads(evidence_path.read_text())
        previous = evidence.get('interaction_checks', {}).get('observed') or {}
        if evidence['case'] != 'C04' or (previous.get('result', {}).get('status') == 'operated' and evidence.get('interaction_check_version') == CHECK_VERSION):
            continue
        source = ROOT / 'runs' / item['run']
        result = json.loads((source / 'result.json').read_text())
        if not (source / 'work/answer.html').exists():
            evidence['interaction_checks'] = {'status': 'no_required_html_file'}
        else:
            driver = (ROOT / 'scripts/check_interaction.mjs').read_text()
            mapping_path = package / 'control-map.json'
            if mapping_path.exists():
                driver = driver.replace('const manual = null;', 'const manual = ' + mapping_path.read_text().strip() + ';')
            (package / 'interaction.js').write_text(driver)
            executions = []
            observations = []
            for width, height in [(1280, 900), (390, 844)]:
                record = prepare_review.render_command(source, result['condition'], package, ['node', '/tools/browser.mjs', 'eval', '/work/answer.html', '/review/interaction.js', str(width), str(height)])
                try:
                    observed = json.loads(record['stdout']) if record['exit'] == 0 else None
                except ValueError:
                    observed = None
                executions.append({'width': width, **record})
                observations.append(observed)
            operated = all(o and o.get('result', {}).get('status') == 'operated' for o in observations)
            merged = {'result': {'status': 'operated' if operated else 'needs_review', 'runs': [r for o in observations if o for r in o.get('result', {}).get('runs', [])]}, 'errors': [e for o in observations if o for e in o.get('errors', [])]}
            evidence['interaction_checks'] = {'executions': executions, 'observed': merged, 'viewport_observations': observations}
        evidence['interaction_check_version'] = CHECK_VERSION
        run.write_json(evidence_path, evidence)
        print(json.dumps({'sample': item['sample'], 'interaction_checked': True}), flush=True)
