from http.server import BaseHTTPRequestHandler,ThreadingHTTPServer
from pathlib import Path
import json
from engine import SCENARIOS,simulate,infer
class Handler(BaseHTTPRequestHandler):
    def send_data(self,data,status=200,kind='application/json'):
        body=json.dumps(data).encode() if kind=='application/json' else data
        self.send_response(status);self.send_header('Content-Type',kind+'; charset=utf-8');self.send_header('X-Content-Type-Options','nosniff');self.send_header('Content-Length',str(len(body)));self.end_headers();self.wfile.write(body)
    def do_GET(self):
        if self.path=='/':self.send_data(Path(__file__).with_name('index.html').read_bytes(),kind='text/html')
        elif self.path=='/api/scenarios':self.send_data([simulate(n) for n in SCENARIOS])
        else:self.send_data({'error':'Not found'},404)
    def do_POST(self):
        if self.path!='/api/infer':return self.send_data({'error':'Not found'},404)
        try:
            size=int(self.headers.get('Content-Length','0'))
            if not 0<size<=20000:raise ValueError()
            data=json.loads(self.rfile.read(size))
            if not isinstance(data,dict):raise ValueError()
        except (ValueError,UnicodeError):return self.send_data({'error':'Input non valido'},400)
        self.send_data(infer(data.get('prompt')))
if __name__=='__main__':ThreadingHTTPServer(('127.0.0.1',8000),Handler).serve_forever()
