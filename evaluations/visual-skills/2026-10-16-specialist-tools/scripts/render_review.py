"""Render finished attempts offline without modifying generated deliverables."""
from pathlib import Path
import json
import subprocess
import run

ROOT = Path(__file__).resolve().parents[1]
run.core.SOCKET_PATH = ROOT / 'review/render-placeholder.sock'
run.core.SOCKET_PATH.touch(exist_ok=True)
records_path = ROOT / 'review/renders.json'
records = json.loads(records_path.read_text()) if records_path.exists() else []
done = {(x['run'], x['source']) for x in records}
for result_path in sorted((ROOT / 'runs').glob('*/result.json')):
    result = json.loads(result_path.read_text())
    folder = result_path.parent
    review = ROOT / 'review' / folder.name
    review.mkdir(exist_ok=True)
    sources = [p for p in (folder / 'work').rglob('*') if p.suffix in ['.html', '.svg'] and p.is_file() and 'tmp' not in p.relative_to(folder / 'work').parts]
    for index, source in enumerate(sorted(sources)):
        relative = str(source.relative_to(folder / 'work'))
        if (folder.name, relative) in done:
            continue
        image_name = f'{index:02d}-{source.stem}.png'
        args = ['node', '/tools/browser.mjs', 'screenshot', '/work/' + relative, '/review/' + image_name, '1600', '1000']
        command = run.command(folder, result['condition'], args)
        i = command.index('--chdir')
        command[i:i] = ['--bind', str(review), '/review']
        try:
            output = subprocess.run(command, env=run.core.environment(), capture_output=True, text=True, timeout=45)
            (review / (image_name + '.log')).write_text(output.stdout + output.stderr)
            record = {'run': folder.name, 'source': relative, 'exit': output.returncode, 'image': str((review / image_name).relative_to(ROOT))}
            if output.returncode == 0:
                record['browser'] = json.loads(output.stdout)
            else:
                record['error'] = output.stderr
        except subprocess.TimeoutExpired:
            record = {'run': folder.name, 'source': relative, 'exit': 'timeout'}
        records.append(record)
        records_path.write_text(json.dumps(records, ensure_ascii=False, indent=2))
        print(json.dumps({k: v for k, v in record.items() if k != 'browser'}, ensure_ascii=False), flush=True)
