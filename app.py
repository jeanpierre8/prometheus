import http.server
from prometheus_client import start_http_server
import random
from prometheus_client import Counter
from prometheus_client import Gauge
from prometheus_client import Summary
import time

INPROGRESS = Gauge('hello_worlds_inprogress', 'Number of Hello Worlds in progress.')
LAST = Gauge('hello_world_last_time_seconds', 'The last time a Hello World was served.')
LATENCY = Summary('hello_world_latency_seconds', 'Time for a request Hello World.')
REQUESTS = Counter('hello_worlds_total', 'Hello worlds requested.')
EXCEPTIONS = Counter('hello_word_excpetions_total', 'Exceptions serving Hello World.')
class MyHandler(http.server.BaseHTTPRequestHandler):
    def do_GET(self):
        start = time.time()
        INPROGRESS.inc()
        REQUESTS.inc(5)  #  Increment
        with EXCEPTIONS.count_exceptions():
            if random.random() < 0.2:
                raise Exception
        self.send_response(200)
        self.end_headers()
        self.wfile.write(b"Hello world")
        LAST.set(time.time())
        INPROGRESS.dec()
        LATENCY.observe(time.time() - start)

if __name__  == "__main__":
    start_http_server(8010) #  Start an HTTP server on the 8000 port to provide services to Promethes Metrics
    server = http.server.HTTPServer(('localhost', 8011), MyHandler)
    server.serve_forever()