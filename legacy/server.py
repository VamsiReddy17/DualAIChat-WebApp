import http.server
import socketserver
import os
from threading import Timer
import webbrowser

PORT = 8080
FRONTEND_DIR = "frontend"

class MyHandler(http.server.SimpleHTTPRequestHandler):
    def do_GET(self):
        if self.path == "/":
            self.path = "/index.html"
        return super().do_GET()

os.chdir(FRONTEND_DIR)

def open_browser():
    webbrowser.open(f"http://localhost:{PORT}")

if __name__ == "__main__":
    Timer(1.5, open_browser).start()
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        print(f"🌐 Frontend running at http://localhost:{PORT}")
        httpd.serve_forever()
