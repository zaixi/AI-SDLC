"""Run the frozen comparison using OpenCode, offline tools, and a host-only API relay."""
from pathlib import Path
from concurrent.futures import ThreadPoolExecutor, as_completed
import argparse
import hashlib
import http.server
import json
import os
import random
import re
import shutil
import signal
import socketserver
import subprocess
import tempfile
import threading
import time
import urllib.request
import urllib.error

ROOT = Path(__file__).resolve().parents[1]
BINARY = Path('/home/liyujiang/.opencode/bin/opencode')
MODEL = 'grok-4.7'
CONDITIONS = ['visual-explanation']
BASE = 'You are an assistant. Complete the user task accurately. Use available tools when useful. Respect the requested output format.'
TOOLS = 'Local tools: Python 3, Node.js 20, Graphviz, Chromium. For HTML/SVG/Mermaid screenshots or Playwright interaction use node /tools/browser.mjs help. Local Mermaid bundle: /tools/mermaid.min.js. Input files are read-only; /work is writable.'
STATE = {}
LOCK = threading.Lock()
PROVIDER = None
MOCK = False
SOCKET_PATH = None
OUTPUT_BUDGET = 131072
REQUEST_LIMIT = 64
TIMEOUT = 900
PLAYWRIGHT = Path('/home/liyujiang/.npm/_npx/8ef14e20fba81900/node_modules')
CHROMIUM = Path('/home/liyujiang/.cache/ms-playwright/chromium-1155/chrome-linux')


def write_json(path, value):
    Path(path).write_text(json.dumps(value, ensure_ascii=False, indent=2) + '\n')


def provider():
    result = subprocess.run([str(BINARY), 'debug', 'config', '--pure'], cwd='/tmp', capture_output=True, text=True, timeout=45)
    for i, ch in enumerate(result.stdout):
        if ch != '{':
            continue
        try:
            data, _ = json.JSONDecoder().raw_decode(result.stdout[i:])
            if isinstance(data, dict) and 'provider' in data:
                return data['provider']['llmproxy']
        except ValueError:
            pass
    raise RuntimeError('Existing provider unavailable; raw configuration suppressed')


class UnixServer(socketserver.ThreadingMixIn, socketserver.UnixStreamServer):
    daemon_threads = True


class Relay(http.server.BaseHTTPRequestHandler):
    protocol_version = 'HTTP/1.1'

    def log_message(self, *_):
        pass

    def reply(self, status, payload, stream=False):
        self.send_response(status)
        self.send_header('Content-Type', 'text/event-stream' if stream else 'application/json')
        self.send_header('Content-Length', str(len(payload)))
        self.end_headers()
        self.wfile.write(payload)

    def do_POST(self):
        match = re.fullmatch(r'/([a-f0-9]{16})/v1/chat/completions', self.path)
        if not match or match[1] not in STATE:
            self.send_error(404)
            return
        state = STATE[match[1]]
        body = json.loads(self.rfile.read(int(self.headers['Content-Length'])))
        title = any(m.get('role') == 'system' and str(m.get('content', '')).startswith('You are a title generator.') for m in body.get('messages', []))
        with LOCK:
            index = state['requests']
            state['requests'] += 1
        write_json(state['run'] / f'request-{index:03}.json', body)
        if MOCK or title:
            text = 'OFFLINE_AUDIT_OK'
            payload = {'id': 'audit', 'object': 'chat.completion', 'created': 1, 'model': MODEL, 'choices': [{'index': 0, 'message': {'role': 'assistant', 'content': text}, 'finish_reason': 'stop'}], 'usage': {'prompt_tokens': 0, 'completion_tokens': 0, 'total_tokens': 0}}
            if body.get('stream'):
                chunk = {'id': 'audit', 'object': 'chat.completion.chunk', 'created': 1, 'model': MODEL, 'choices': [{'index': 0, 'delta': {'role': 'assistant', 'content': text}, 'finish_reason': None}]}
                raw = ('data: ' + json.dumps(chunk) + '\n\ndata: [DONE]\n\n').encode()
            else:
                raw = json.dumps(payload).encode()
            self.reply(200, raw, body.get('stream', False))
            return
        if state['model_requests'] >= REQUEST_LIMIT or state['output_tokens'] >= OUTPUT_BUDGET:
            state['budget_exhausted'] = True
            self.reply(400, b'{"error":{"message":"Task generation budget exhausted","type":"budget_exhausted"}}')
            return
        remaining = OUTPUT_BUDGET - state['output_tokens']
        token_field = 'max_completion_tokens' if 'max_completion_tokens' in body else 'max_tokens'
        if body.get(token_field, 65536) > remaining:
            body[token_field] = remaining
            write_json(state['run'] / f'effective-request-{index:03}.json', body)
        state['model_requests'] += 1
        opts = PROVIDER['options']
        headers = {'Content-Type': 'application/json', 'Authorization': 'Bearer ' + opts['apiKey']}
        headers.update(opts.get('headers', {}))
        req = urllib.request.Request(opts['baseURL'].rstrip('/') + '/chat/completions', data=json.dumps(body).encode(), headers=headers, method='POST')
        chunks = []
        started = time.time()
        try:
            with urllib.request.urlopen(req, timeout=240) as response:
                self.send_response(response.status)
                self.send_header('Content-Type', response.headers.get('Content-Type', 'application/json'))
                self.send_header('Connection', 'close')
                self.end_headers()
                while data := response.read1(65536):
                    chunks.append(data)
                    self.wfile.write(data)
                    self.wfile.flush()
        except (urllib.error.HTTPError, urllib.error.URLError, TimeoutError) as error:
            code = getattr(error, 'code', 502)
            write_json(state['run'] / f'upstream-error-{index:03}.json', {'status': code, 'type': type(error).__name__})
            if not chunks:
                self.reply(code, json.dumps({'error': {'message': f'Evaluation upstream HTTP {code}', 'type': 'upstream_error'}}).encode())
        except (BrokenPipeError, ConnectionResetError):
            pass
        finally:
            self.close_connection = True
            raw = b''.join(chunks)
            (state['run'] / f'response-{index:03}.txt').write_bytes(raw)
            usage = {}
            reasons = []
            records = [raw] if not body.get('stream') else [line[6:] for line in raw.splitlines() if line.startswith(b'data: ') and line[6:] != b'[DONE]']
            for record in records:
                try:
                    value = json.loads(record)
                except ValueError:
                    continue
                if value.get('usage'):
                    usage = value['usage']
                reasons += [c['finish_reason'] for c in value.get('choices', []) if c.get('finish_reason')]
            state['output_tokens'] += usage.get('completion_tokens', 0)
            write_json(state['run'] / f'usage-{index:03}.json', {'usage': usage, 'finish_reasons': reasons, 'seconds': round(time.time() - started, 3)})


def environment():
    return {'HOME': '/home/eval', 'USER': 'eval', 'LANG': 'C.UTF-8', 'PATH': '/runtime/node/bin:/usr/bin:/bin', 'PYTHONPATH': '/runtime/python', 'NODE_PATH': '/runtime/node_modules', 'ARCHIFY_CHROME': '/runtime/chromium/chrome', 'ARCHIFY_CHROME_NO_SANDBOX': '1', 'CHROME_PATH': '/runtime/chromium/chrome', 'PUPPETEER_EXECUTABLE_PATH': '/runtime/chromium/chrome', 'PLAYWRIGHT_CHROMIUM_EXECUTABLE_PATH': '/runtime/chromium/chrome', 'SHELL': '/bin/bash',
            'OPENCODE_DISABLE_AUTOUPDATE': 'true', 'OPENCODE_DISABLE_MODELS_FETCH': 'true', 'OPENCODE_DISABLE_DEFAULT_PLUGINS': 'true', 'OPENCODE_DISABLE_CLAUDE_CODE': 'true',
            'OPENCODE_EXPERIMENTAL_OUTPUT_TOKEN_MAX': '65536'}


def setup(run, condition, case):
    for rel in ['home/.config/opencode', 'home/.cache/opencode', 'work', 'input/fixtures', 'tools']:
        (run / rel).mkdir(parents=True, exist_ok=True)
    for fixture in case.get('fixtures', []):
        shutil.copy2(ROOT / 'inputs/fixtures' / fixture, run / 'input/fixtures' / fixture)
    manifest = json.loads((ROOT / 'manifest.json').read_text())
    for rel in manifest['generation_skill_allowlist'][condition]:
        dst = run / 'input/skill' / rel
        dst.parent.mkdir(parents=True, exist_ok=True)
        shutil.copy2(ROOT / 'snapshots' / condition / rel, dst)
    catalog = []
    if condition == 'visual-explanation':
        (run / 'input/specialists').mkdir()
        for name in manifest['generation_specialist_allowlist'][condition]:
            path = ROOT / 'dependencies/skills' / name / 'SKILL.md'
            source = path.read_text()
            import yaml
            metadata = yaml.safe_load(source.split('---', 2)[1])
            assert not metadata.get('disable-model-invocation'), name
            catalog.append({'name': metadata['name'], 'description': metadata['description'], 'path': f'/input/specialists/{name}/SKILL.md'})
    (run / 'home/.cache/opencode/models.json').write_text('{}\n')
    extra = '\nAvailable optional skills; read the listed SKILL.md when needed:\n' + json.dumps(catalog, ensure_ascii=False) if catalog else ''
    config = {'$schema': 'https://opencode.ai/config.json', 'model': 'evaluation/' + MODEL, 'small_model': 'evaluation/' + MODEL,
              'enabled_providers': ['evaluation'], 'autoupdate': False, 'share': 'disabled', 'snapshot': False, 'plugin': [], 'instructions': [],
              'provider': {'evaluation': {'npm': '@ai-sdk/openai-compatible', 'name': 'Evaluation relay', 'options': {'baseURL': 'http://127.0.0.1:18761/v1', 'apiKey': 'non-secret-placeholder'},
                            'models': {MODEL: {'name': MODEL, 'options': {'reasoningEffort': 'high'}, 'limit': {'context': 450000, 'output': 65536}, 'modalities': {'input': ['text', 'image'], 'output': ['text']}}}}},
              'agent': {'eval': {'description': 'Complete the current task', 'mode': 'primary', 'prompt': BASE + '\n' + TOOLS + extra,
                         'permission': {'*': 'deny', 'read': 'allow', 'write': 'allow', 'edit': 'allow', 'bash': 'allow', 'glob': 'allow', 'grep': 'allow', 'list': 'allow', 'external_directory': 'allow'}}},
              'default_agent': 'eval', 'formatter': False, 'lsp': False}
    write_json(run / 'home/.config/opencode/opencode.json', config)
    write_json(run / 'catalog-audit.json', catalog)
    for name in ['browser.mjs', 'sandbox_bridge.py']:
        shutil.copy2(ROOT / 'scripts' / name, run / 'tools' / name)
    shutil.copy2(ROOT / 'dependencies/runtime/mermaid.min.js', run / 'tools/mermaid.min.js')
    return config


def command(run, condition, args):
    cmd = ['bwrap', '--die-with-parent', '--unshare-all', '--ro-bind', '/usr', '/usr', '--symlink', 'usr/bin', '/bin', '--ro-bind', '/lib', '/lib', '--ro-bind', '/lib64', '/lib64',
           '--proc', '/proc', '--dev', '/dev', '--tmpfs', '/tmp', '--dir', '/etc', '--ro-bind', '/etc/alternatives', '/etc/alternatives', '--ro-bind', '/etc/fonts', '/etc/fonts',
           '--ro-bind', str(BINARY), '/opt/opencode', '--bind', str(run / 'home'), '/home/eval', '--bind', str(run / 'work'), '/work', '--ro-bind', str(run / 'input'), '/input',
           '--ro-bind', str(run / 'tools'), '/tools', '--ro-bind', str(SOCKET_PATH), '/run/model.sock',
           '--ro-bind', str(PLAYWRIGHT / 'playwright'), '/runtime/node_modules/playwright', '--ro-bind', str(PLAYWRIGHT / 'playwright-core'), '/runtime/node_modules/playwright-core',
           '--ro-bind', str(CHROMIUM), '/runtime/chromium']
    if condition == 'visual-explanation':
        cmd += ['--ro-bind', str(ROOT / 'dependencies/skills'), '/input/specialists']
    return cmd + ['--chdir', '/work', '--', *args]


def audit_fs(run, condition):
    probe = '''import json,pathlib,shutil,socket
p=pathlib.Path
paths=["/home/liyujiang", "/input/skill/SKILL.md", "/input/skill/references/evaluation.md", "/input/specialists/mermaid-diagrams/SKILL.md", "/input/specialists/diagram-design/SKILL.md", "/input/specialists/answer-me-with-html/scripts/am.mjs", "/home/eval/.codex/skills", "/home/eval/.agents/skills", "/home/eval/.config/opencode/skills"]
out={"paths":{x:p(x).exists() for x in paths},"am_in_path":shutil.which("am"),"interfaces":socket.if_nameindex()}
sock=socket.socket();sock.settimeout(1)
try:sock.connect(("1.1.1.1",443));out["external_network"]=True
except OSError:out["external_network"]=False
print(json.dumps(out))'''
    result = subprocess.run(command(run, condition, ['/usr/bin/python3', '-c', probe]), env=environment(), capture_output=True, text=True, timeout=15, check=True)
    report = json.loads(result.stdout)
    paths = report['paths']
    assert paths['/input/skill/SKILL.md'] == (condition != 'none')
    assert all(value == (condition == 'visual-explanation') for key, value in paths.items() if key.startswith('/input/specialists/'))
    assert not any(value for key, value in paths.items() if key.startswith('/home/') or key.endswith('/evaluation.md'))
    assert not report['external_network'] and not report['am_in_path']
    assert report['interfaces'] == [[1, 'lo']]
    write_json(run / 'filesystem-audit.json', report)


def execute(job, preflight=False):
    run = ROOT / ('preflight' if preflight else 'runs') / job['id']
    if run.exists():
        raise RuntimeError('Refusing to overwrite ' + str(run))
    run.mkdir(parents=True)
    key = hashlib.sha256(job['id'].encode()).hexdigest()[:16]
    state = {'run': run, 'requests': 0, 'model_requests': 0, 'output_tokens': 0, 'budget_exhausted': False}
    STATE[key] = state
    setup(run, job['condition'], job)
    audit_fs(run, job['condition'])
    prompt = '完成下面的用户请求。输入文件只读；需要文件产物时写入 /work，并在最终回复给出文件路径。只完成当前请求。\n\n'
    if job['condition'] != 'none':
        prompt = '请先读取并遵守 /input/skill/SKILL.md，完成实际文件交付。\n\n' + prompt
    prompt += job['prompt']
    if job.get('delivery') == 'html':
        prompt += '\n\n文件交付位置：/work/answer.html。'
    if job.get('delivery') == 'svg':
        prompt += '\n\n文件交付位置：/work/answer.svg。'
    (run / 'prompt.txt').write_text(prompt)
    launch = 'python3 /tools/sandbox_bridge.py "$1" > /tmp/bridge.log 2>&1 &\nexec /opt/opencode run --pure --format json --agent eval -m evaluation/grok-4.7 "$2"'
    launch = launch.replace('evaluation/grok-4.7', 'evaluation/' + MODEL)
    args = ['/bin/bash', '-c', launch, 'eval-launch', key, prompt]
    started = time.time()
    with (run / 'events.jsonl').open('w') as out, (run / 'stderr.log').open('w') as err:
        proc = subprocess.Popen(command(run, job['condition'], args), env=environment(), stdout=out, stderr=err, start_new_session=True)
        try:
            code = proc.wait(timeout=90 if preflight else TIMEOUT)
            try: os.killpg(proc.pid, signal.SIGTERM)
            except ProcessLookupError: pass
        except subprocess.TimeoutExpired:
            os.killpg(proc.pid, signal.SIGTERM)
            try:
                proc.wait(timeout=10)
            except subprocess.TimeoutExpired:
                os.killpg(proc.pid, signal.SIGKILL)
                proc.wait()
            code = 'timeout'
    events = []
    for line in (run / 'events.jsonl').read_text().splitlines():
        try:
            events.append(json.loads(line))
        except ValueError:
            pass
    texts = [e['part']['text'] for e in events if e.get('type') == 'text']
    (run / 'answer.md').write_text('\n\n'.join(texts) + '\n')
    result = {**job, 'exit': code, 'seconds': round(time.time() - started, 2), 'requests': state['requests'], 'model_requests': state['model_requests'],
              'output_tokens': state['output_tokens'], 'budget_exhausted': state['budget_exhausted'], 'has_text': bool(texts),
              'artifacts': [str(p.relative_to(run / 'work')) for p in (run / 'work').rglob('*') if p.is_file()], 'errors': [e for e in events if e.get('type') == 'error']}
    write_json(run / 'result.json', result)
    print(json.dumps({k: result[k] for k in ['id', 'exit', 'seconds', 'model_requests', 'has_text', 'budget_exhausted']}, ensure_ascii=False), flush=True)
    return result


def audit_requests(results):
    reports = []
    for result in results:
        run = ROOT / 'preflight' / result['id']
        requests = sorted(run.glob('request-*.json'))
        assert requests, result['id']
        raw = next(p.read_text() for p in requests if json.loads(p.read_text()).get('tools'))
        body = json.loads(raw)
        assert body['model'] == MODEL
        assert body.get('max_tokens', body.get('max_completion_tokens')) == 65536
        assert all(x not in raw for x in ['2026-10-10-dual-model', '/home/liyujiang', 'skill-creator', 'oh-my-opencode'])
        for name in ['mermaid-diagrams', 'diagram-design', 'answer-me-with-html']:
            assert (name in raw) == (result['condition'] == 'visual-explanation'), (result['id'], name)
        assert [t['function']['name'] for t in body['tools']] == ['bash', 'read', 'glob', 'grep', 'edit', 'write']
        reports.append({'condition': result['condition'], 'model': MODEL, 'max_tokens': body.get('max_tokens', body.get('max_completion_tokens')), 'tools': [t['function']['name'] for t in body['tools']], 'specialist_metadata_correct': True, 'requests': len(requests)})
    write_json(ROOT / 'preflight/request-audit.json', reports)


def main():
    global PROVIDER, MOCK, SOCKET_PATH
    parser = argparse.ArgumentParser()
    parser.add_argument('mode', choices=['audit', 'probe', 'run'])
    parser.add_argument('--label', default='')
    args = parser.parse_args()
    MOCK = args.mode == 'audit'
    if not MOCK:
        PROVIDER = provider()
    relay_dir = Path(tempfile.mkdtemp(prefix='ve-relay-'))
    SOCKET_PATH = relay_dir / 'api.sock'
    server = UnixServer(str(SOCKET_PATH), Relay)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    try:
        if args.mode == 'audit':
            jobs = [{'id': 'audit-' + args.label + c, 'condition': c, 'prompt': 'Reply only OK. Do not use tools.', 'fixtures': []} for c in CONDITIONS]
        elif args.mode == 'probe':
            jobs = [{'id': 'live-probe' + args.label, 'condition': 'none', 'prompt': 'Reply only OK. Do not use tools.', 'fixtures': []}]
        else:
            assert (ROOT / 'preflight/request-audit.json').exists(), 'Run offline audit first'
            cases = json.loads((ROOT / 'inputs/cases.json').read_text())['cases']
            jobs = []
            for rep in range(1, 2):
                for case in cases:
                    conditions = CONDITIONS.copy()
                    random.Random(f'visual-content-{rep}-{case["id"]}').shuffle(conditions)
                    for condition in conditions:
                        jobs.append({**case, 'case': case['id'], 'id': f'r{rep}-{case["id"]}-{condition}', 'condition': condition, 'repeat': rep})
            write_json(ROOT / 'jobs.json', jobs)
            jobs = [j for j in jobs if not (ROOT / 'runs' / j['id'] / 'result.json').exists()]
        with ThreadPoolExecutor(max_workers=3) as pool:
            results = [f.result() for f in as_completed([pool.submit(execute, j, args.mode != 'run') for j in jobs])]
        if MOCK:
            audit_requests(results)
    finally:
        server.shutdown()
        server.server_close()
        SOCKET_PATH.unlink(missing_ok=True)
        relay_dir.rmdir()


if __name__ == '__main__':
    main()
