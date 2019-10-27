from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs


class mHandler(BaseHTTPRequestHandler):
    def do_HEAD(self):
        self.send_response(200)
        self.send_header("Content-type", "text/html")
        self.end_headers()

    def do_GET(self):
        print(self.path)
        parsed = parse_qs(urlparse(self.path).query)

        print(parsed)
        self.respond({"status": 200})

    def respond(self, opts):
        self.wfile.write(bytes(str(opts), "UTF-8"))


def run(server_class=HTTPServer):
    server_address = ("", 8080)
    httpd = server_class(server_address, mHandler)
    print("Listening on port 8080")
    httpd.serve_forever()


run()