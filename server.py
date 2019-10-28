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
        self.send_header("Access-Control-Allow-Origin", "*")
        self.end_headers()

    def do_GET(self):
        # Listens to route /search, ignores rest
        if self.path.startswith("/search"):
            # Filters GET request parameters
            parsed = parse_qs(urlparse(self.path).query)
            # Query parameter must have been specified in order to process the query
            if "query" in parsed and len(parsed["query"]) > 0:
                self.respond(qh.query(index, parsed["query"][0], documents))                
            else:
                self.respond({"hits": {}})

    def respond(self, content):
        self._set_headers_()
        self.wfile.write(bytes(json.dumps(content), "UTF-8"))


def run(args, server_class=HTTPServer):
    global index, documents
    server_address = ("", int(args.port))
    httpd = server_class(server_address, mHandler)
    index = load_inverse_file(args.index)  # TF-IDF inverse file
    documents = load_documents(args.documents)  # Just a simple dictionary to match document_ids with their content
    print("Listening on port " + str(args.port))
    httpd.serve_forever()


def parse_args():
    parser = argparse.ArgumentParser(description="Web server configuration")
    parser.add_argument("-i", "--index", default="index.json", help="Document collection to queries")
    parser.add_argument("-d", "--documents", default="cran-1400.txt", help="Corpus of documents")
    parser.add_argument("-p", "--port", default=8080, help="Port number")
    args = parser.parse_args()
    return args


run(parse_args())

