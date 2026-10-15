"""Make anonymous evidence packages and render unmodified outputs offline."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
from html.parser import HTMLParser
import hashlib
import json
import re
import shutil
import subprocess
from PIL import Image
import run

ROOT = run.ROOT
REVIEW = ROOT / 'review'
EXPECTATIONS = json.loads((ROOT / 'judge/expectations.json').read_text())['cases']


class CodeBlocks(HTMLParser):
    def __init__(self):
        super().__init__()
        self.blocks = []
        self.active = None

    def handle_starttag(self, tag, attrs):
        if tag == 'pre':
            self.active = []

    def handle_data(self, data):
        if self.active is not None:
            self.active.append(data)

    def handle_endtag(self, tag):
        if tag == 'pre' and self.active is not None:
            self.blocks.append(''.join(self.active))
            self.active = None


def anonymize(text):
    text = re.sub(r'/home/[^\s)"<>]+/skill-evaluations/[^\s)"<>]+', '[artifact-path]', text)
    return re.sub(r'(?i)\b(?:visual-explanation|show-me|mermaid-diagrams|diagram-design|answer-me-with-html)\b', '[skill]', text)


def delivered_answer(source_run):
    events = []
    for line in (source_run / 'events.jsonl').read_text().splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    stops = [e['part']['messageID'] for e in events if e.get('type') == 'step_finish' and e['part'].get('reason') == 'stop']
    texts = [e['part'] for e in events if e.get('type') == 'text']
    if stops:
        return '\n\n'.join(p['text'] for p in texts if p['messageID'] == stops[-1]), 'final_stop_message'
    # Recover only the latest model response; retain CLI delivery provenance.
    requests = [p for p in sorted(source_run.glob('request-*.json'))
                if json.loads(p.read_text()).get('tools')]
    if requests:
        response = requests[-1].with_name(requests[-1].name.replace('request-', 'response-').replace('.json', '.txt'))
        chunks, reasons = [], []
        if response.exists():
            for line in response.read_text().splitlines():
                if not line.startswith('data: ') or line == 'data: [DONE]':
                    continue
                try:
                    record = json.loads(line[6:])
                except ValueError:
                    continue
                for choice in record.get('choices', []):
                    if choice.get('index') == 0:
                        chunks.append(choice.get('delta', {}).get('content') or '')
                        reasons.append(choice.get('finish_reason'))
            if 'stop' in reasons and ''.join(chunks).strip():
                return ''.join(chunks), 'provider_stream_recovered_cli_text_missing'
    return '\n\n'.join(p['text'] for p in texts), 'partial_visible_messages_no_final_stop'


def named_artifacts(source_run, answer):
    extensions = ('.html', '.svg', '.png', '.mmd', '.md', '.txt', '.py')
    tokens = re.findall(r'(?:/work/|/home/eval/)[^\s\)\]<>`"\']+\.(?:html|svg|png|mmd|md|txt|py)', answer)
    tokens += re.findall(r'(?<!`)`([^`\n]+)`(?!`)', answer)
    tokens += re.findall(r'\]\(([^)]+)\)', answer)
    paths = []
    for token in tokens:
        token = token.removeprefix('file://')
        if Path(token).suffix not in extensions:
            continue
        if token.startswith('/work/'):
            candidate = source_run / 'work' / token[len('/work/'):]
        elif token.startswith('/home/eval/'):
            candidate = source_run / 'home' / token[len('/home/eval/'):]
        elif not token.startswith('/') and '://' not in token:
            candidate = source_run / 'work' / token
        else:
            continue
        allowed = any(candidate.resolve().is_relative_to((source_run / directory).resolve()) for directory in ('work', 'home'))
        if allowed and candidate.is_file() and candidate not in paths:
            paths.append(candidate)
    for candidate in (source_run / 'work').rglob('*'):
        if candidate.suffix in extensions and candidate.is_file() and candidate.name in answer and candidate not in paths:
            if candidate.resolve().is_relative_to((source_run / 'work').resolve()):
                paths.append(candidate)
    return paths


def render_command(source_run, condition, package, args):
    run.SOCKET_PATH = Path('/dev/null')
    command = run.command(source_run, condition, args)
    index = command.index('--chdir')
    command[index:index] = ['--bind', str(package), '/review']
    try:
        result = subprocess.run(command, env=run.environment(), capture_output=True, text=True, timeout=60)
        return {'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
    except subprocess.TimeoutExpired:
        return {'exit': 'timeout', 'stdout': '', 'stderr': 'Review command exceeded 60 seconds; render/check unverified.'}


def prepare(source_run):
    result = json.loads((source_run / 'result.json').read_text())
    ident = 'S' + hashlib.sha256(('blind-content-v2:' + result['id']).encode()).hexdigest()[:10]
    package = REVIEW / 'anonymous' / ident
    if (package / 'evidence.json').exists() and json.loads((package / 'evidence.json').read_text()).get('evidence_version') == 6:
        return {'sample': ident, 'run': result['id']}
    package.mkdir(parents=True, exist_ok=True)
    answer, reply_scope = delivered_answer(source_run)
    (package / 'answer.md').write_text(anonymize(answer))
    (package / 'all-messages.md').write_text(anonymize((source_run / 'answer.md').read_text()))
    for name in result.get('fixtures', []):
        dst = package / 'fixtures' / name
        dst.parent.mkdir(exist_ok=True)
        shutil.copy2(ROOT / 'inputs/fixtures' / name, dst)
    artifacts = []
    delivery = result.get('delivery')
    if delivery in ('html', 'svg'):
        expected = source_run / 'work' / ('answer.' + delivery)
        paths = [expected] if expected.exists() else []
    else:
        # Include explicitly named relative files as well as absolute links.
        paths = [p for p in named_artifacts(source_run, answer) if p.suffix != '.py' or result['case'] == 'A04']
    if reply_scope == 'partial_visible_messages_no_final_stop' and not paths:
        paths = sorted(p for p in (source_run / 'work').iterdir() if p.is_file() and p.suffix in ('.html', '.svg'))
        paths += sorted((source_run / 'home/.answer-me-with-html/pages').glob('*.html'))
    sources = []
    for index, path in enumerate(paths):
        name = f'artifact-{index}{path.suffix}'
        shutil.copy2(path, package / name)
        original = '/work/' + str(path.relative_to(source_run / 'work')) if path.is_relative_to(source_run / 'work') else '/home/eval/' + str(path.relative_to(source_run / 'home'))
        sources.append({'source': name, 'kind': 'mermaid' if path.suffix == '.mmd' else path.suffix[1:], '_render_input': original})
    for index, block in enumerate(re.findall(r'```mermaid[^\n]*\n(.*?)```', answer, re.S)):
        name = f'diagram-{index}.mmd'
        (package / name).write_text(block)
        sources.append({'source': name, 'kind': 'mermaid'})
    for source in list(sources):
        if source['kind'] == 'md':
            for index, block in enumerate(re.findall(r'```mermaid[^\n]*\n(.*?)```', (package / source['source']).read_text(), re.S)):
                name = f'{Path(source["source"]).stem}-diagram-{index}.mmd'
                (package / name).write_text(block)
                sources.append({'source': name, 'kind': 'mermaid', 'source_document': source['source']})
    for source in sources:
        renders = []
        if source['kind'] in ('md', 'txt', 'py'):
            artifacts.append({**{k: v for k, v in source.items() if not k.startswith('_')}, 'renders': []})
            continue
        if source['kind'] == 'png':
            with Image.open(package / source['source']) as bitmap:
                renders.append({'width': bitmap.width, 'height': bitmap.height, 'screenshot': source['source'], 'details': None,
                                'exit': 0, 'stdout': '', 'stderr': '', 'native_png': True})
            artifacts.append({**{k: v for k, v in source.items() if not k.startswith('_')}, 'renders': renders})
            continue
        for width, height in [(1280, 900), (390, 844)]:
            output = f'{Path(source["source"]).stem}-{width}.png'
            command = ['node', '/tools/browser.mjs', 'screenshot', source.get('_render_input', '/review/' + source['source']), '/review/' + output, str(width), str(height)]
            record = render_command(source_run, result['condition'], package, command)
            try:
                details = json.loads(record['stdout']) if record['exit'] == 0 else None
            except ValueError:
                details = None
            renders.append({'width': width, 'height': height, 'screenshot': output if (package / output).exists() else None, 'details': details, **record})
        artifacts.append({**{k: v for k, v in source.items() if not k.startswith('_')}, 'renders': renders})
    code_checks = None
    ui_checks = None
    chart_checks = None
    portability_checks = None
    if delivery == 'html' and paths:
        shutil.copy2(ROOT / 'scripts/check_portability.mjs', package / 'portability-check.js')
        portability_checks = []
        for width, height in [(1280, 900), (390, 844)]:
            record = render_command(source_run, result['condition'], package, ['node', '/tools/browser.mjs', 'eval', '/review/artifact-0.html', '/review/portability-check.js', str(width), str(height)])
            try:
                observed = json.loads(record['stdout']) if record['exit'] == 0 else None
            except ValueError:
                observed = None
            portability_checks.append({'width': width, 'observed': observed, 'exit': record['exit'], 'stderr': record['stderr']})
    if result['case'] in ('C01', 'C03') and paths:
        shutil.copy2(ROOT / 'scripts/check_chart.mjs', package / 'chart-check.js')
        chart_checks = []
        for width, height in [(1280, 900), (390, 844)]:
            record = render_command(source_run, result['condition'], package, ['node', '/tools/browser.mjs', 'eval', '/work/answer.html', '/review/chart-check.js', str(width), str(height)])
            try:
                observed = json.loads(record['stdout']) if record['exit'] == 0 else None
            except ValueError:
                observed = None
            chart_checks.append({'width': width, 'observed': observed, 'exit': record['exit'], 'stderr': record['stderr']})
    if result['case'] == 'C02' and paths:
        shutil.copy2(ROOT / 'scripts/check_ui.mjs', package / 'ui-check.js')
        ui_checks = []
        for width, height in [(1280, 900), (390, 844)]:
            record = render_command(source_run, result['condition'], package, ['node', '/tools/browser.mjs', 'eval', '/work/answer.html', '/review/ui-check.js', str(width), str(height)])
            try:
                observed = json.loads(record['stdout']) if record['exit'] == 0 else None
            except ValueError:
                observed = None
            ui_checks.append({'width': width, 'observed': observed, 'exit': record['exit'], 'stderr': record['stderr']})
    if result['case'] == 'A04':
        fences = re.findall(r'^```([^\n]*)\n(.*?)^```[ \t]*$', answer, re.S | re.M)
        blocks = [body for language, body in fences if language.strip() in ('python', 'py', '')]
        for path in paths:
            if path.suffix == '.py':
                blocks.append(path.read_text())
            if path.suffix in ('.md', '.txt'):
                fences = re.findall(r'^```([^\n]*)\n(.*?)^```[ \t]*$', path.read_text(), re.S | re.M)
                blocks += [body for language, body in fences if language.strip() in ('python', 'py', '')]
            if path.suffix == '.html':
                parser = CodeBlocks()
                parser.feed(path.read_text())
                blocks += parser.blocks
        code = next((b for b in blocks if re.search(r'^def encode_runs\(', b, re.M)), '')
        if code:
            tests = EXPECTATIONS['A04']['code_checks']
            harness = code + '\n\nimport json\nchecks = ' + repr(tests) + '\nreport=[]\nfor check in checks:\n expected=[tuple(x) for x in check["expected"]]\n actual=encode_runs(check["input"])\n report.append({"input":check["input"],"pass":actual==expected,"actual":repr(actual),"expected":repr(expected)})\nprint(json.dumps(report))\n'
            (package / 'function-check.py').write_text(harness)
            code_checks = render_command(source_run, result['condition'], package, ['python3', '/review/function-check.py'])
        else:
            code_checks = {'exit': None, 'error': 'No complete encode_runs function could be extracted'}
    api_failure = bool(list(source_run.glob('upstream-error-*.json'))) or 'APIConnectionError' in json.dumps(result.get('errors', []))
    evidence = {'evidence_version': 6, 'sample': ident, 'case': result['case'], 'prompt': result['prompt'], 'fixtures': result.get('fixtures', []), 'delivery': delivery, 'reply_scope': reply_scope,
                'expected_file_present': bool(paths) if delivery in ('html', 'svg') else None,
                'generation_ended': 'timeout' if result['exit'] == 'timeout' else 'finished', 'budget_exhausted': result['budget_exhausted'],
                'infrastructure_failure': api_failure and not answer.strip() and not artifacts,
                'artifacts': artifacts, 'code_checks': code_checks, 'ui_checks': ui_checks, 'chart_checks': chart_checks, 'portability_checks': portability_checks}
    if (package / 'evidence.json').exists():
        previous = json.loads((package / 'evidence.json').read_text())
        if 'interaction_checks' in previous:
            evidence['interaction_checks'] = previous['interaction_checks']
            evidence['interaction_check_version'] = previous.get('interaction_check_version')
    run.write_json(package / 'evidence.json', evidence)
    print(json.dumps({'sample': ident, 'case': result['case'], 'artifacts': len(artifacts)}), flush=True)
    return {'sample': ident, 'run': result['id']}


if __name__ == '__main__':
    REVIEW.mkdir(exist_ok=True)
    sources = sorted(p.parent for p in (ROOT / 'runs').glob('*/result.json'))
    with ThreadPoolExecutor(max_workers=1) as pool:
        records = [f.result() for f in as_completed([pool.submit(prepare, p) for p in sources])]
    run.write_json(REVIEW / 'private-mapping.json', records)
    print(json.dumps({'prepared': len(records)}))
