from http.server import BaseHTTPRequestHandler, HTTPServer
import re
import redis
from http.cookies import SimpleCookie
import uuid
from urllib.parse import parse_qsl, urlparse
import json
mappings = {
        (r"^/books/(?P<book_id>\d+)$", "get_books"),
        (r"^/$", "index"),
        (r"^/search", "search")
        }

r = redis.StrictRedis(host="localhost", port=6379, db=0)

class WebRequestHandler(BaseHTTPRequestHandler):
     
    @property
    def url(self):
        return urlparse(self.path)

    @property 
    def query_data(self):
        return dict(parse_qsl(self.url.query))


    def cookies(self):
        return SimpleCookie(self.headers.get("Cookie"))

    def get_session(self):
        cookies = self.cookies()
        session_id = None
        if not cookies:
            session_id = uuid.uuid4()
        else:
            session_id = cookies["session_id"].value
        return session_id
            
    def write_session_cookie(self, session_id):
        cookies = SimpleCookie()
        cookies["session_id"] = session_id
        cookies["session_id"]["max-age"] = 1000
        self.send_header("Set-Cookie", cookies.output(header=""))

# Inicio
    def do_GET(self):
        self.url_mapping_response()

# Mapeo de rutas
    def url_mapping_response(self):
        # (pattern, method)
        for pattern, method in mappings:
            match = self.get_params(pattern, self.path)
            # Si existe la ruta
            if match is not None:
                md = getattr(self, method)
                md(**match)
                return
        # Sino error 404
        self.send_response(404)
        # self.send_header("Content-Type", "text/html")
        self.end_headers()
        error = f"<h1> Not found </h1>".encode("utf-8")
        self.wfile.write(error)

# Checa si la ruta coincide con el patrón
    def get_params(self, pattern, path):
        match = re.match(pattern, path)
        if match:
            return match.groupdict()

# /books/\d+
    def get_books(self, book_id):
        # Obtiene las recomendaciones de libros
        def getRecomended():
            session_id = self.get_session()
            category = self.retrieve_book_category(book_id)
            bookKey = f"{book_id}"

            booksInCategory = r.get(category)
            booksInCategory = json.loads(booksInCategory)       

            self.wfile.write("<h3>Recomendados</h3>".encode("utf-8"))

            for book in booksInCategory:
                if book is bookKey:
                    continue
                bookContent = r.get(book)
                bookTitle = re.search(r"(?<=<h2>)(.*)(?=</h2>)", bookContent.decode('utf-8'))
                self.wfile.write(f"<br> <a href=/books/{book}> Libro {book}: {bookTitle.group()} </a>".encode("utf-8"))
            return book_info, book_list, session_id

        # Obtiene el historial de libros
        def getHistory():
            session_id = self.get_session()
            bookKey = f"{book_id}"
            book_list = r.lrange(f"session: {session_id}", 0, -1)
                
            self.wfile.write("<h3>Historial</h3>".encode("utf-8"))
            for book in book_list:
                if book is bookKey.encode('utf-8'):
                    continue
                bookContent = r.get(book)
                bookTitle = re.search(r"(?<=<h2>)(.*)(?=</h2>)", bookContent.decode('utf-8'))
                self.wfile.write(f"<br> <a href=/books/{book.decode()}> Libro {book.decode()}: {bookTitle.group()} </a>".encode("utf-8"))
            return book_info, book_list, session_id

#######################################################
        
        session_id = self.get_session()
        bookKey = f"{book_id}"
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.write_session_cookie(session_id)
        self.end_headers()
        book_info = r.get(bookKey) or "<h1> No existe el libro </h1>".encode("utf-8")
        self.wfile.write(book_info)
        # self.wfile.write(f"<br>session: {session_id}".encode("utf-8"))
        book_list = r.lrange(f"session: {session_id}", 0, -1)

        if bookKey.encode('utf-8') not in book_list:
            r.lpush(f"session: {session_id}", bookKey)
        # for book in book_list:
            # self.wfile.write(f"<br> book: {book}".encode("utf-8"))
            
        getRecomended()
        getHistory()
    
#  /
    def index(self):
        self.send_response(200)
        self.send_header("Content-Type", "text/html")
        self.end_headers()
        with open('html/index.html') as f:
            response = f.read()
        self.wfile.write(response.encode("utf-8"))

# /search
    def search(self):
        query_key = self.query_data.get('q')
        if query_key:
            html_content = self.searchBooks(query_key)
            if html_content:
                self.send_response(200)
                self.send_header("Content-Type", "text/html")
                self.end_headers()
                self.wfile.write(html_content)
                return

        self.send_response(404)
        self.end_headers()
        error_message = "<h1>La clave no existe o no se proporcionó.</h1>"
        self.wfile.write(error_message.encode("utf-8"))
    def retrieve_book_category(self, book_id):
        # redis variable
        json_string = r.get(f'book_data:{book_id}')
        if json_string:
            book_data = json.loads(json_string)
            return book_data["categoria"]
        else:
            return None
# Buscar libros
    def searchBooks(self, query):
        resultado = []
        values = r.keys("[1-999999]")
        # values = r.keys()
        print (values)
        for value in values:
            
            libro = r.get(value)
            if libro and query.lower() in libro.decode('utf-8').lower():
                book_data = json.loads(r.get(f'book_data:{value.decode("utf-8")}'))
                resultado.append(f"<a href=/books/{value.decode('utf-8')}>{book_data['nombre']}</a>")

        return f"<h2>Resultados</h2><br>{resultado}".encode("utf-8")


if __name__ == "__main__":
    print("Server starting...")
    server = HTTPServer(("0.0.0.0", 8000), WebRequestHandler)
    server.serve_forever()
