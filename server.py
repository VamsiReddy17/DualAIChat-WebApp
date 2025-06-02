
#!/usr/bin/env python3
import http.server
import socketserver
import os
import webbrowser
from threading import Timer

PORT = 5000
DIRECTORY = "frontend"

class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)
    
    def end_headers(self):
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        super().end_headers()
    
    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

def open_browser():
    webbrowser.open(f'http://0.0.0.0:{PORT}')

if __name__ == "__main__":
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    try:
        # Allow port reuse to prevent "Address already in use" errors
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
            print(f"🚀 Server running at http://0.0.0.0:{PORT}")
            print(f"📁 Serving files from: {DIRECTORY}")
            print("🤖 Dual AI Chatbots Interface Ready!")
            print("\n⚠️  Note: Backend Azure Functions need to be running separately for full functionality")
            
            # Open browser after a short delay
            Timer(1.5, open_browser).start()
            
            try:
                httpd.serve_forever()
            except KeyboardInterrupt:
                print("\n👋 Server stopped")
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use. Trying to kill existing process...")
            import subprocess
            try:
                subprocess.run(["pkill", "-f", "server.py"], check=False)
                print("🔄 Retrying frontend server startup...")
                import time
                time.sleep(2)
                with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
                    print(f"🚀 Server running at http://0.0.0.0:{PORT}")
                    httpd.serve_forever()
            except Exception as retry_e:
                print(f"❌ Failed to restart frontend server: {retry_e}")
                raise
        else:
            print(f"❌ Frontend server startup error: {e}")
            raise
