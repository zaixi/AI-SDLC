from pathlib import Path
import json,re,hashlib,xml.etree.ElementTree as ET,difflib
b=Path('/workspace/AI-SDLC/evaluations/visual-skills/2026-10-15-v2-expanded');original=(b/'inputs/fixtures/notification-flow.svg').read_text();allowed={'failure','failure-label'}
def canonical(e):return [e.tag,sorted(e.attrib.items()),(e.text or '').strip(),[canonical(c) for c in e if c.attrib.get('id') not in allowed]]
root=ET.fromstring(original);results=[];sources=[]
for c in ['v042','candidate']:
 text=(b/'outputs'/c/'03-svg-edit.md').read_text();source=re.findall(r'```svg\s*\n([\s\S]*?)```',text)[0];sources.append(source);new=ET.fromstring(source);assert canonical(root)==canonical(new)
 old_by_id={e.attrib['id']:e for e in root.iter() if 'id' in e.attrib};new_by_id={e.attrib['id']:e for e in new.iter() if 'id' in e.attrib}
 changed=[k for k in old_by_id if ET.tostring(old_by_id[k])!=ET.tostring(new_by_id[k])];assert set(changed)==allowed
 assert new_by_id['failure-label'].text=='通知失败：仅重试通知';assert new_by_id['failure'].attrib['d']=='M690 150 V225 Q690 245 670 245 H630 Q610 245 610 225 V150'
 results.append({'condition':c,'xml':'passed','outside_failure_and_label_equal':True,'changed_id_elements':changed,'failure_start':[690,150],'failure_end':[610,150],'notify_bounds':[560,80,740,150],'endpoints_touch_notify_not_execute':True,'label':new_by_id['failure-label'].text,'original_to_final_diff':'\n'.join(difflib.unified_diff(original.strip().splitlines(),source.strip().splitlines(),fromfile='original',tofile=c))})
(b/'svg-edit-review.json').write_text(json.dumps({'method':'Canonical XML compares all elements except failure path and its label; ignores indentation-only tails, retains all other text/style/attributes. Endpoints traced from exact path to target node bounds. Actual PNG also inspected.','results':results,'final_svg_identical_between_conditions':sources[0]==sources[1]},ensure_ascii=False,indent=2)+'\n');print(json.dumps({'outside_change_scope_preserved':True,'two_sources_identical':sources[0]==sources[1]},ensure_ascii=False))
