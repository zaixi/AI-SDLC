from pathlib import Path
import subprocess,json
ROOT=Path(__file__).resolve().parents[1]
CHECKS={
"R01":r'''import csv,io,sys,unittest
sys.path.insert(0,"/work")
from inventory.export import export_products
rows=[{"sku":"001","name":"A,B","quantity":3},{"sku":"002","name":'a"b\nc',"quantity":0},{"sku":"三","name":"书","quantity":-2}]
expected=[["sku","name","quantity"],["001","A,B","3"],["002",'a"b\nc',"0"],["三","书","-2"]]
for source in [rows,(x for x in rows)]:
    actual=export_products(source)
    assert isinstance(actual,str)
    assert list(csv.reader(io.StringIO(actual)))==expected,repr(actual)
assert list(csv.reader(io.StringIO(export_products(iter([])))))==[["sku","name","quantity"]]
suite=unittest.defaultTestLoader.discover("/work/tests")
result=unittest.TextTestRunner().run(suite)
assert result.wasSuccessful()
print("PASS CSV escaping, generator, empty input, Unicode; existing tests")
''',
"R02":r'''import pathlib,tempfile,subprocess,zipfile,sys
p=pathlib.Path
with tempfile.TemporaryDirectory() as tmp:
    base=p(tmp); src=base/"source";src.mkdir();(src/"nested").mkdir()
    (src/"书.txt").write_text("hello");(src/"nested/a.txt").write_text("world")
    (base/"secret.txt").write_text("outside")
    (src/"link.txt").symlink_to(base/"secret.txt")
    (src/"linkdir").symlink_to(src/"nested",target_is_directory=True)
    for dest in [base/"out.zip",src/"output.zip"]:
        for existing in [False,True]:
            if existing:dest.write_bytes(b"old archive")
            result=subprocess.run([sys.executable,"/work/pack.py",str(src),str(dest)],capture_output=True,text=True)
            assert result.returncode==0,(result.stdout,result.stderr)
            with zipfile.ZipFile(dest) as z:
                names={n for n in z.namelist() if not n.endswith("/")}
                assert names=={"书.txt","nested/a.txt"},names
                assert z.read("书.txt")==b"hello"
                assert z.read("nested/a.txt")==b"world"
print("PASS nested files, relative paths, Unicode, file/directory symlinks, output-inside-source including existing destination")
'''}
results=[]
for run in sorted((ROOT/"runs").glob("*")):
    case=run.name.split("-")[0]
    if case not in CHECKS or not (run/"result.json").exists():continue
    cmd=["bwrap","--die-with-parent","--unshare-all","--ro-bind","/usr","/usr","--symlink","usr/bin","/bin","--ro-bind","/lib","/lib","--ro-bind","/lib64","/lib64","--ro-bind","/etc/alternatives","/etc/alternatives","--proc","/proc","--dev","/dev","--tmpfs","/tmp","--ro-bind",str(run/"work"),"/work","--chdir","/work","--","/usr/bin/python3","-c",CHECKS[case]]
    proc=subprocess.run(cmd,capture_output=True,text=True,timeout=25)
    results.append({"id":run.name,"exit":proc.returncode,"stdout":proc.stdout,"stderr":proc.stderr})
(ROOT/"review/behavior-checks.json").write_text(json.dumps(results,ensure_ascii=False,indent=2))
print(json.dumps(results,ensure_ascii=False,indent=2))
