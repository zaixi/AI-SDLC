"""Prepare a fresh external evaluation directory from committed lightweight inputs."""
from pathlib import Path
import argparse,hashlib,json,shutil

SOURCE=Path(__file__).resolve().parents[1]
parser=argparse.ArgumentParser()
parser.add_argument('destination',type=Path)
args=parser.parse_args()
root=args.destination.expanduser().resolve()
root.mkdir(parents=True,exist_ok=False)
for folder in ['scripts','inputs']:shutil.copytree(SOURCE/folder,root/folder)
(root/'review').mkdir()
shutil.copy2(SOURCE/'RUBRIC.md',root/'review/RUBRIC.md')
shutil.copy2(SOURCE/'inputs/checks.py',root/'review/checks.py')
rules=json.loads((SOURCE/'inputs/rules.json').read_text())
for condition,body in rules.items():
    folder=root/'snapshots'/condition;folder.mkdir(parents=True)
    (folder/'AGENTS.md').write_text(body)
protocol=json.loads((SOURCE/'protocol.json').read_text())
protocol.pop('postprocessing_sha256',None)
protocol.update(status='prepared',raw_directory=str(root))
paths=list((root/'scripts').glob('*.py'))+list((root/'inputs').glob('*'))+list((root/'snapshots').rglob('*.md'))+list((root/'review').glob('*'))
protocol['sha256']={str(p.relative_to(root)):hashlib.sha256(p.read_bytes()).hexdigest() for p in paths if p.is_file()}
(root/'protocol.json').write_text(json.dumps(protocol,indent=2))
print(root)
