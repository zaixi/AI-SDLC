"""Restore an isolated run from the archived runtime/source bundle, not old answers."""
from pathlib import Path
import argparse
import hashlib
import json
import shutil

SOURCE = Path(__file__).resolve().parents[1]
parser = argparse.ArgumentParser()
parser.add_argument('archive', type=Path, help='Original external evaluation directory or restored bundle')
parser.add_argument('destination', type=Path, help='A new directory, must not exist')
args = parser.parse_args()
archive = args.archive.expanduser().resolve()
destination = args.destination.expanduser().resolve()
protocol = json.loads((SOURCE / 'protocol.json').read_text())
for relative, expected in protocol['sha256'].items():
    if not relative.startswith(('snapshots/', 'specialists/')):
        continue
    path = archive / relative
    if hashlib.sha256(path.read_bytes()).hexdigest() != expected:
        raise SystemExit('Snapshot mismatch: ' + relative)
destination.mkdir(parents=True, exist_ok=False)
for folder in ['snapshots', 'specialists', 'runtime']:
    shutil.copytree(archive / folder, destination / folder, ignore=shutil.ignore_patterns('__pycache__'))
for folder in ['inputs', 'scripts']:
    shutil.copytree(SOURCE / folder, destination / folder, ignore=shutil.ignore_patterns('__pycache__'))
(destination / 'review').mkdir()
shutil.copy2(SOURCE / 'RUBRIC.md', destination / 'review/RUBRIC.md')
protocol.update(status='prepared', raw_directory=str(destination), replay_source=str(archive))
(destination / 'protocol.json').write_text(json.dumps(protocol, ensure_ascii=False, indent=2))
print(destination)
