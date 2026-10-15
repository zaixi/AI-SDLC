from pathlib import Path
import importlib.util,re,json,sys
b=Path('/workspace/AI-SDLC/evaluations/visual-skills/2026-10-10-native-diagram-design');spec=importlib.util.spec_from_file_location('geo',b/'inputs/verify-geometry.py');m=importlib.util.module_from_spec(spec);sys.modules['geo']=m;spec.loader.exec_module(m);r=json.loads((b/'geometry-scope-review.json').read_text());coverage=[]
for f in sorted((b/'trajectories').glob('*/*/stage*/answer.md')):
 for i,html in enumerate(re.findall(r'```html\s*\n([\s\S]*?)```',f.read_text()),1):
  connectors=m.connectors(html);coverage.append({'answer':str(f.relative_to(b)),'html_block':i,'recognized_connector_count':len(connectors),'note':'Only explicit marker-start/end attributes are recognized. CSS-defined arrows ignored; zero count is not validation of actual connections.'})
r['connector_coverage']=coverage;r['implementation_evidence']='verify-geometry.py shapes() does not tag independent root SVG coordinate spaces; stacked_connectors() compares global pairs. connectors() requires inline marker attributes, not CSS marker declarations.';(b/'geometry-scope-review.json').write_text(json.dumps(r,ensure_ascii=False,indent=2)+'\n');print(json.dumps(coverage,ensure_ascii=False,indent=2))
