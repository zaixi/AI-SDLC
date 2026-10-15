import io,json,os,sys,tempfile,unittest,urllib.error,importlib
from pathlib import Path
from unittest.mock import patch
sys.path.insert(0,'/work')
CASE=sys.argv.pop(1)


class Client(unittest.TestCase):
    def error(self,code,headers=None):
        return urllib.error.HTTPError('https://example',code,'error',headers or {},None)

    def call(self,responses):
        import ticket_client
        self.request=patch('urllib.request.urlopen',side_effect=responses)
        self.sleep=patch('time.sleep')
        return ticket_client.get_ticket

    def test_429_then_success(self):
        f=self.call([self.error(429,{'Retry-After':'2'}),io.BytesIO(b'{"id":8}')])
        with self.request as request,self.sleep as sleep:
            self.assertEqual(f('https://example/',8),{'id':8});self.assertEqual(request.call_count,2);sleep.assert_called_once_with(2)
            self.assertTrue(all(c.kwargs['timeout']==10 for c in request.call_args_list))

    def test_header_fallback_and_cap(self):
        for header,delay in [(None,1),('bad',1),('-1',1),('1.5',1),('0',0),('100',2)]:
            with self.subTest(header=header):
                f=self.call([self.error(429,{} if header is None else {'Retry-After':header}),io.BytesIO(b'{}')])
                with self.request,self.sleep as sleep:f('https://example',1);sleep.assert_called_once_with(delay)

    def test_three_attempts_last_error(self):
        errors=[self.error(429)]*2+[self.error(429)]
        f=self.call(errors)
        with self.request as request,self.sleep as sleep:
            with self.assertRaises(urllib.error.HTTPError) as ctx:f('https://example',1)
            self.assertIs(ctx.exception,errors[-1]);self.assertEqual(request.call_count,3);self.assertEqual(sleep.call_count,2)

    def test_404_and_other_errors_unchanged(self):
        for code in [404,400,401,500,503]:
            with self.subTest(code=code):
                error=self.error(code);f=self.call([error])
                with self.request as request,self.sleep as sleep:
                    if code==404:self.assertIsNone(f('https://example',1))
                    else:
                        with self.assertRaises(urllib.error.HTTPError) as ctx:f('https://example',1)
                        self.assertIs(ctx.exception,error)
                    self.assertEqual(request.call_count,1);sleep.assert_not_called()

    def test_network_error_unchanged(self):
        error=urllib.error.URLError('offline');f=self.call([error])
        with self.request as request,self.sleep as sleep:
            with self.assertRaises(urllib.error.URLError) as ctx:f('https://example',1)
            self.assertIs(ctx.exception,error);self.assertEqual(request.call_count,1);sleep.assert_not_called()


class Settings(unittest.TestCase):
    def run_load(self,env):
        import settings
        with tempfile.TemporaryDirectory() as tmp:
            path=Path(tmp)/'settings.json';body=json.dumps({'log_level':'custom-file-level','database':{'options':[1,2]},'other':True})
            path.write_text(body)
            try:
                with patch.dict(os.environ,env,clear=True):return settings.load_settings(path)
            finally:self.assertEqual(path.read_text(),body)

    def test_unset_empty_preserve(self):
        for env in [{},{'APP_LOG_LEVEL':''}]:self.assertEqual(self.run_load(env)['log_level'],'custom-file-level')

    def test_valid_preserves_other_keys(self):
        for level in ['DEBUG','INFO','WARNING','ERROR']:
            self.assertEqual(self.run_load({'APP_LOG_LEVEL':level,'APP_DATABASE':'wrong'}),{'log_level':level,'database':{'options':[1,2]},'other':True})

    def test_invalid(self):
        for value in ['debug',' WARN ','CRITICAL',' INFO',' ']:
            with self.subTest(value=value):
                with self.assertRaisesRegex(ValueError,'APP_LOG_LEVEL'):self.run_load({'APP_LOG_LEVEL':value})

    def test_missing_file_unchanged(self):
        import settings
        with patch.dict(os.environ,{},clear=True):
            with self.assertRaises(FileNotFoundError):settings.load_settings('/tmp/does-not-exist-ablation.json')


class Archive(unittest.TestCase):
    def test_legacy_current_cwd(self):
        import archivekit
        old=os.getcwd()
        try:
            with tempfile.TemporaryDirectory() as a,tempfile.TemporaryDirectory() as b:
                for folder in [a,b]:
                    os.chdir(folder);self.assertIsNone(archivekit.archive(b'old','nested/a'));self.assertEqual(Path('archives/nested/a').read_bytes(),b'old')
        finally:os.chdir(old)

    def test_multiple_memory_instances(self):
        from archivekit import create_archive,MemoryBackend
        a,b=MemoryBackend(),MemoryBackend();fa,fb=create_archive(a),create_archive(b)
        self.assertIsNone(fa(b'one','k'));fb(b'two','k');fa(b'three','k')
        self.assertEqual(a.records,{'k':b'three'});self.assertEqual(b.records,{'k':b'two'})

    def test_local_backend(self):
        from archivekit import create_archive,LocalBackend
        with tempfile.TemporaryDirectory() as tmp:
            save=create_archive(LocalBackend(tmp));save(b'a','nested/x');save(b'b','nested/x')
            self.assertEqual((Path(tmp)/'nested/x').read_bytes(),b'b')

    def test_external_consumer(self):
        from archivekit import create_archive
        source='''from archivekit import Backend
class CustomerBackend(Backend):
    def __init__(self): self.calls=[]
    def write(self,data: bytes,key: str) -> None: self.calls.append((data,key))
'''
        with tempfile.TemporaryDirectory() as tmp:
            p=Path(tmp)/'customer_backend.py';p.write_text(source)
            spec=importlib.util.spec_from_file_location('customer_backend',p);module=importlib.util.module_from_spec(spec);spec.loader.exec_module(module)
            backend=module.CustomerBackend();save=create_archive(backend);save(b'customer','a/b');self.assertEqual(backend.calls,[(b'customer','a/b')])

    def test_exception_identity(self):
        from archivekit import create_archive
        error=RuntimeError('backend failed')
        class FailedBackend:
            def write(self,data,key):raise error
        save=create_archive(FailedBackend())
        with self.assertRaises(RuntimeError) as ctx:save(b'a','k')
        self.assertIs(ctx.exception,error)


suite=unittest.defaultTestLoader.loadTestsFromTestCase({'N01':Client,'N02':Settings,'N03':Archive}[CASE])
result=unittest.TextTestRunner(verbosity=2).run(suite)
raise SystemExit(not result.wasSuccessful())
