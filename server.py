from http.server import HTTPServer, BaseHTTPRequestHandler
from urllib.parse import urlparse, parse_qs
from queries.index_persistence import load_inverse_file, load_documents
from queries import query_handler as qh
import json
import argparse


'''
    Basic web server that listens to GET petitinos at this endpoint:
        \search?query=XXXXX
    and returns the matching documents as a JSON response
'''

index = {}
documents = {}


class mHandler(BaseHTTPRequestHandler):
    def _set_headers_(self):
        self.send_response(200)
        self.send_header("Content-type", "application/json")
        self.end_headers()

    def do_GET(self):
        print(self.path)
        if self.path.startswith("/search"):
            parsed = parse_qs(urlparse(self.path).query)
            print(parsed["query"][0])
            result = qh.query(index, parsed["query"][0], documents)
            self._set_headers_()
            self.wfile.write(bytes(json.dumps(result), "UTF-8"))


def run(args, server_class=HTTPServer):
    global index, documents
    server_address = ("", int(args.port))
    httpd = server_class(server_address, mHandler)
    index = load_inverse_file(args.index)  # TF-IDF inverse file
    documents = load_documents(args.documents)  # Just a simple dictionary to match document_ids with their content
    print("Listening on port " + args.port)
    httpd.serve_forever()


def parse_args():
    parser = argparse.ArgumentParser(description="Web server configuration")
    parser.add_argument("-i", "--index", default="index.json", help="Document collection to queries")
    parser.add_argument("-d", "--documents", default="cran-1400.txt", help="Corpus of documents")
    parser.add_argument("-p", "--port", default=8080, help="Port number")
    args = parser.parse_args()
    return args


run(parse_args())

