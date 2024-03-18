from functools import cached_property
from http.cookies import SimpleCookie
from urllib.parse import parse_qsl, urlparse
from http.server import BaseHTTPRequestHandler, HTTPServer
from urllib.parse import parse_qsl, urlparse

# Código basado en:
# https://realpython.com/python-http-server/
# https://docs.python.org/3/library/http.server.html
# https://docs.python.org/3/library/http.cookies.html


class WebRequestHandler(BaseHTTPRequestHandler):
    @property
    def query_data(self):
        return dict(parse_qsl(self.url.query))
    
    @property
    def url(self):
        return urlparse(self.url.query)
    
    def search(self):
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        index.page = f"<h1>{self.path}</h1>".encode("uft-8") 
        self.wfile.write(index_page)
    
    def get_params(self, pattern, path):
        match = re.match(pattern, path)
        if match:
            return match.groupdict()
    
    def index(self):
        self.send_response(200)
        self.send_header("content-type", "text/html")
        self.end_headers()
        index_page = """
        <h1>Bienvenidos a la Biblioteca</h1>
        form"""

    @cached_property
    def url(self):
        return urlparse(self.path)

    @cached_property
    def query_data(self):
        return dict(parse_qsl(self.url.query))

    @cached_property
    def post_data(self):
        content_length = int(self.headers.get("Content-Length", 0))
        return self.rfile.read(content_length)

    @cached_property
    def form_data(self):
        return dict(parse_qsl(self.post_data.decode("utf-8")))

    @cached_property
    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        self.wfile.write(self.get_response().encode("utf-8"))

    def get_response(self):
        return f"""
    <h1> Hola Web </h1>
    <p>  {self.path}         </p>
    <p>  {self.headers}      </p>
    <p>  {self.cookies}      </p>
    <p>  {self.query_data}   </p>
"""


# Hola

if __name__ == "__main__":
    print("Server starting...")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()




from http.server import HTTPServer, BaseHTTPRequestHandler

class WebRequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write('<h1>Hola {self.path}</h1>'.encode("utf-8"))

if __name__ == '__main__':
    print('Iniciando servidor...')
    server = HTTPServer(('0.0.0.0', 8000), WebRequestHandler)
    server.serve_forever()