import unittest,io,urllib.error
from unittest.mock import patch,MagicMock
from engine import simulate,infer,SCENARIOS
class Tests(unittest.TestCase):
    def test_scenarios(self):
        for name,status in SCENARIOS.items():
            with self.subTest(name=name):self.assertEqual(simulate(name)['status'],status)
    def test_unknown(self):self.assertEqual(simulate([])['status'],400)
    def test_invalid(self):
        for value in ('',None,42,'x'*4001):self.assertEqual(infer(value)['status'],422)
    @patch.dict('os.environ',{},clear=True)
    def test_demo(self):self.assertEqual(infer('hello')['outcome'],'fallback')
    @patch.dict('os.environ',{'HF_TOKEN':'test'})
    @patch('urllib.request.urlopen')
    def test_http_errors(self,call):
        for status in (401,403,404,429,500,503):
            call.side_effect=urllib.error.HTTPError('https://example.invalid',status,'error',{},None)
            self.assertEqual(infer('hello')['status'],status)
    @patch.dict('os.environ',{'HF_TOKEN':'test'})
    @patch('urllib.request.urlopen',side_effect=TimeoutError)
    def test_timeout(self,call):self.assertEqual(infer('hello')['outcome'],'fallback')
    @patch.dict('os.environ',{'HF_TOKEN':'test'})
    @patch('urllib.request.urlopen')
    def test_response(self,call):
        response=call.return_value.__enter__.return_value
        response.read.return_value=b'{"choices":[{"message":{"content":"ok"}}]}'
        self.assertEqual(infer('hello')['text'],'ok')
        response.read.return_value=b'bad'
        self.assertEqual(infer('hello')['status'],502)
