#!/usr/bin/python

from http.server import HTTPServer, CGIHTTPRequestHandler

HOST = "127.0.0.1"
PORT = 29997
SERVER_ADDRESS = (HOST, PORT)

server = HTTPServer(SERVER_ADDRESS, CGIHTTPRequestHandler)
server.serve_forever()