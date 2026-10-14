"""Exercise condition visibility and bundled tools without any model calls."""
from pathlib import Path
import argparse
import json
import socket
import subprocess
import tempfile
import run


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--label', default='')
    args = parser.parse_args()
    directory = Path(tempfile.mkdtemp(prefix='ve-smoke-'))
    sock = socket.socket(socket.AF_UNIX, socket.SOCK_STREAM)
    run.SOCKET_PATH = directory / 'api.sock'
    sock.bind(str(run.SOCKET_PATH))
    reports = []
    try:
        for condition in run.CONDITIONS:
            root = run.ROOT / 'preflight' / ('runtime-' + args.label + condition)
            root.mkdir(parents=True, exist_ok=False)
            run.setup(root, condition, {'fixtures': []})
            run.audit_fs(root, condition)
            (root / 'work/smoke.html').write_text('<!doctype html><meta charset="utf-8"><title>Render check</title><p>渲染检查 · 42</p>')
            (root / 'work/smoke.mmd').write_text('flowchart LR\n  S[开始] --> E[完成]\n')
            (root / 'work/smoke.svg').write_text('<svg xmlns="http://www.w3.org/2000/svg" width="1200" height="500" viewBox="0 0 1200 500"><rect width="1200" height="500" fill="white"/><text x="30" y="80" font-size="32">独立 SVG 检查</text><circle cx="1150" cy="450" r="30" fill="green"/></svg>')
            commands = [
                ['node', '--version'],
                ['node', '/tools/browser.mjs', 'screenshot', '/work/smoke.html', '/work/html.png', '390', '844'],
                ['node', '/tools/browser.mjs', 'screenshot', '/work/smoke.mmd', '/work/mermaid.png'],
                ['node', '/tools/browser.mjs', 'screenshot', '/work/smoke.svg', '/work/svg-desktop.png'],
                ['node', '/tools/browser.mjs', 'screenshot', '/work/smoke.svg', '/work/svg-mobile.png', '390', '844'],
            ]
            if condition == 'visual-explanation':
                commands.append(['node', '/input/specialists/answer-me-with-html/scripts/am.mjs', 'help'])
                (root / 'work/draft.md').write_text('---\ntitle: 后端检查\nlang: zh\n---\n## 一个步骤\n```flow\n接收 -> 完成: 处理\n```\n')
                commands.append(['node', '/input/specialists/answer-me-with-html/scripts/am.mjs', 'render', '/work/draft.md', '--no-open', '-o', '/work/backend.html'])
                commands.append(['node', '/tools/browser.mjs', 'screenshot', '/work/backend.html', '/work/backend.png'])
            results = []
            for index, command in enumerate(commands):
                result = subprocess.run(run.command(root, condition, command), env=run.environment(), capture_output=True, text=True, timeout=45)
                record = {'command': command, 'exit': result.returncode, 'stdout': result.stdout, 'stderr': result.stderr}
                run.write_json(root / f'tool-{index}.json', record)
                if result.returncode:
                    raise RuntimeError(json.dumps({'condition': condition, **record}, ensure_ascii=False))
                results.append(record)
            reports.append({'condition': condition, 'filesystem': 'passed', 'network': 'offline', 'tools_exercised': len(results)})
            print(json.dumps(reports[-1]), flush=True)
        run.write_json(run.ROOT / 'preflight/runtime-audit.json', reports)
    finally:
        sock.close()
        run.SOCKET_PATH.unlink(missing_ok=True)
        directory.rmdir()


if __name__ == '__main__':
    main()
