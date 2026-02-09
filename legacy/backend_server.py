import http.server
import socketserver
import json
import os
import requests
from dotenv import load_dotenv

load_dotenv()

PORT = int(os.getenv("PORT", 8000))

AZURE_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
DEEPSEEK_ENDPOINT = os.getenv("DEEPSEEK_ENDPOINT")

class MyHandler(http.server.BaseHTTPRequestHandler):
    def _set_headers(self, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        self.send_response(200)
        self.send_header("Content-type", "text/plain")
        self.end_headers()
        self.wfile.write("✅ Backend server is running.".encode("utf-8"))


    def do_POST(self):
        content_length = int(self.headers.get('Content-Length', 0))
        body = self.rfile.read(content_length)
        try:
            data = json.loads(body)
        except:
            self._set_headers(400)
            self.wfile.write(b'{"error": "Invalid JSON"}')
            return

        if self.path == "/api/ChatGpt_api":
            print("🔁 ChatGPT Request")
            resp = requests.post(
                AZURE_ENDPOINT,
                headers={
                    "Content-Type": "application/json",
                    "api-key": AZURE_KEY
                },
                json=data
            )
        elif self.path == "/api/DeepSeek_api":
            print("🔁 DeepSeek Request")
            resp = requests.post(
                DEEPSEEK_ENDPOINT,
                headers={"Content-Type": "application/json"},
                json=data
            )
        else:
            self._set_headers(404)
            self.wfile.write(b'{"error": "Not Found"}')
            return

        self._set_headers(resp.status_code)
        self.wfile.write(resp.content)

if __name__ == "__main__":
    print(f"🚀 Backend server running at http://localhost:{PORT}")
    with socketserver.TCPServer(("", PORT), MyHandler) as httpd:
        httpd.serve_forever()
