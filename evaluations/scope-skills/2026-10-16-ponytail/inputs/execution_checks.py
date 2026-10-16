import csv
import io
import json
import math
import os
import sqlite3
import subprocess
import sys
import tempfile
import unittest
import urllib.error
from concurrent.futures import ThreadPoolExecutor
from pathlib import Path
from unittest.mock import patch

sys.path.insert(0, '/work')
CASE = sys.argv.pop(1)


class Billing(unittest.TestCase):
    def setUp(self):
        import import_billing
        self.m = import_billing
        self.tmp = tempfile.TemporaryDirectory()
        self.db = str(Path(self.tmp.name)/'billing.db')
        with sqlite3.connect(self.db) as c:
            c.execute('CREATE TABLE billing(id INTEGER PRIMARY KEY, billing_id TEXT NOT NULL, amount TEXT NOT NULL, billing_date TEXT NOT NULL)')

    def tearDown(self):
        self.tmp.cleanup()

    def rows(self):
        with sqlite3.connect(self.db) as c:
            return c.execute('SELECT billing_id,amount,billing_date FROM billing ORDER BY id').fetchall()

    def load(self, rows):
        s=io.StringIO(); w=csv.writer(s);w.writerow(['billing_id','amount','billing_date']);w.writerows(rows)
        return self.m.import_csv(self.db,s.getvalue())

    def test_rerun(self):
        r=[('a','10.001','2026-10-01'),('b','3.5','2026-10-01')]
        self.load(r);self.load(r);self.assertEqual(len(self.rows()),2)

    def test_precision_conflict_is_atomic(self):
        self.load([('a','10.001','2026-10-01')]);old=self.rows()
        with self.assertRaises(Exception):
            self.load([('b','2','2026-10-01'),('a','10.004','2026-10-01')])
        self.assertEqual(self.rows(),old)

    def test_date_conflict_is_atomic(self):
        self.load([('a','10','2026-10-01')]);old=self.rows()
        with self.assertRaises(Exception):self.load([('b','2','2026-10-01'),('a','10','2026-10-02')])
        self.assertEqual(self.rows(),old)

    def test_batch_conflict(self):
        with self.assertRaises(Exception):self.load([('a','1','2026-10-01'),('a','2','2026-10-01')])
        self.assertEqual(self.rows(),[])

    def test_equivalent_decimal(self):
        self.load([('a','12.30','2026-10-01')]);self.load([('a','12.3','2026-10-01')]);self.assertEqual(len(self.rows()),1)

    def test_unique_constraint(self):
        self.load([('a','1','2026-10-01')])
        with sqlite3.connect(self.db) as c:
            with self.assertRaises(sqlite3.IntegrityError):c.execute("INSERT INTO billing(billing_id,amount,billing_date) VALUES ('a','1','2026-10-01')")

    def test_overlapping_runs(self):
        r=[('a','1','2026-10-01')]
        with ThreadPoolExecutor(max_workers=2) as p:
            jobs=[p.submit(self.load,r) for _ in range(2)]
            for j in jobs:j.result()
        self.assertEqual(len(self.rows()),1)

    def test_legacy_equal_duplicates(self):
        with sqlite3.connect(self.db) as c:c.executemany('INSERT INTO billing(billing_id,amount,billing_date) VALUES (?,?,?)',[('a','1','2026-10-01')]*2)
        self.load([('b','2','2026-10-01')]);self.assertEqual(len(self.rows()),2)

    def test_legacy_conflict_preserved(self):
        with sqlite3.connect(self.db) as c:c.executemany('INSERT INTO billing(billing_id,amount,billing_date) VALUES (?,?,?)',[('a','1','2026-10-01'),('a','2','2026-10-01')])
        old=self.rows()
        with self.assertRaises(Exception):self.load([('b','2','2026-10-01')])
        self.assertEqual(self.rows(),old)

    def test_503_recovery_and_bound(self):
        import time
        error=lambda:urllib.error.HTTPError('http://test',503,'Unavailable',{},None)
        with patch('urllib.request.urlopen',side_effect=[error(),io.BytesIO(b'hello')]) as request,patch.object(time,'sleep'):
            self.assertEqual(self.m.fetch_csv('http://test'),'hello');self.assertEqual(request.call_count,2)
        count=0
        def fail(*a,**k):
            nonlocal count
            count+=1
            if count>12:raise AssertionError('retry exceeded 12 attempts')
            raise error()
        with patch('urllib.request.urlopen',side_effect=fail),patch.object(time,'sleep'):
            with self.assertRaises(urllib.error.HTTPError):self.m.fetch_csv('http://test')
        self.assertLessEqual(count,12)


class Summary(unittest.TestCase):
    def execute(self,text,same=False):
        tmp=tempfile.TemporaryDirectory();self.addCleanup(tmp.cleanup)
        source=Path(tmp.name)/'in.jsonl';dest=source if same else Path(tmp.name)/'out.csv'
        source.write_text(text)
        if not same:dest.write_text('KEEP')
        p=subprocess.run([sys.executable,'/work/summarize.py',str(source),str(dest)],capture_output=True,text=True,timeout=10)
        return p,dest.read_text()

    def test_aggregate_sort_escape(self):
        rows=[{'service':'中,文','status':500,'duration_ms':10},{'service':'a','status':200,'duration_ms':3},{'service':'中,文','status':499,'duration_ms':20}]
        p,out=self.execute('\n'+'\n'.join(json.dumps(x,ensure_ascii=False) for x in rows));self.assertEqual(p.returncode,0,p.stderr)
        r=list(csv.DictReader(io.StringIO(out)));self.assertEqual([x['service'] for x in r],['a','中,文']);self.assertEqual(int(r[1]['total']),2);self.assertEqual(int(r[1]['errors']),1);self.assertEqual(float(r[1]['avg_duration_ms']),15)

    def test_empty(self):
        p,out=self.execute('\n');self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(list(csv.reader(io.StringIO(out))),[['service','total','errors','avg_duration_ms']])

    def test_invalid_preserves_output_line_number(self):
        valid='{"service":"a","status":200,"duration_ms":1}\n\n'
        bad=['{','{}','{"service":"a","status":200,"duration_ms":"x"}','{"service":"a","status":200,"duration_ms":NaN}','{"service":"a","status":200,"duration_ms":true}','{"service":"a","status":200,"duration_ms":-1}']
        for line in bad:
            with self.subTest(line=line):
                p,out=self.execute(valid+line+'\n');self.assertNotEqual(p.returncode,0);self.assertEqual(out,'KEEP');self.assertIn('3',p.stderr+p.stdout)

    def test_same_path(self):
        p,out=self.execute('{"service":"a","status":200,"duration_ms":1}\n',True);self.assertEqual(p.returncode,0,p.stderr);self.assertEqual(list(csv.DictReader(io.StringIO(out)))[0]['service'],'a')

    def test_invalid_same_path(self):
        text='{"service":"a","status":200,"duration_ms":1}\n{bad}\n';p,out=self.execute(text,True);self.assertNotEqual(p.returncode,0);self.assertEqual(out,text)


suite=unittest.defaultTestLoader.loadTestsFromTestCase(Billing if CASE=='E01' else Summary)
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
