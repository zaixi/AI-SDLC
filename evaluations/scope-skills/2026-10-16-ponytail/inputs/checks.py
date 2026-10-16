import runpy,sys
from pathlib import Path
runpy.run_path(str(Path(__file__).with_name('execution_checks.py' if sys.argv[1].startswith('E') else 'ablation_checks.py')),run_name='__main__')
