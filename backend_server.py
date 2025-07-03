#!/usr/bin/env python3
import http.server
import socketserver
import json
import os
import requests
from urllib.parse import urlparse, parse_qs
import threading

# Environment variables (from your secrets)
AZURE_OPENAI_KEY = os.getenv("AZURE_KEY")
AZURE_ENDPOINT = os.getenv("AZURE_ENDPOINT")
DEEPSEEK_ENDPOINT = os.getenv("DEEPSEEK_ENDPOINT")

# Check if environment variables are set
print("🔍 Checking environment variables...")
if not AZURE_OPENAI_KEY:
    print("⚠️  AZURE_KEY not found in environment")
if not AZURE_ENDPOINT:
    print("⚠️  AZURE_ENDPOINT not found in environment") 
if not DEEPSEEK_ENDPOINT:
    print("⚠️  DEEPSEEK_ENDPOINT not found in environment")

if AZURE_OPENAI_KEY and AZURE_ENDPOINT and DEEPSEEK_ENDPOINT:
    print("✅ All environment variables are set!")
else:
    print("⚠️  Some environment variables are missing. API calls will fail until they're set.")

class APIHandler(http.server.BaseHTTPRequestHandler):
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def do_GET(self):
        if self.path == '/':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response_data = {
                "message": "Backend API Server", 
                "status": "running",
                "endpoints": {
                    "chatgpt": "/api/ChatGpt_api",
                    "deepseek": "/api/DeepSeek_api",
                    "health": "/health"
                }
            }
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        elif self.path == '/health':
            self.send_response(200)
            self.send_header('Content-Type', 'application/json')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            response_data = {"status": "healthy", "message": "Backend server is running"}
            self.wfile.write(json.dumps(response_data).encode('utf-8'))
        else:
            self.send_error(404, "Endpoint not found")

    def do_POST(self):
        try:
            if self.path == '/api/ChatGpt_api':
                self.handle_chatgpt()
            elif self.path == '/api/DeepSeek_api':
                self.handle_deepseek()
            else:
                self.send_json_response({"error": "API endpoint not found"}, 404)
        except Exception as e:
            print(f"❌ POST request error: {str(e)}")
            self.send_json_response({"error": "Server error", "details": str(e)}, 500)

    def handle_chatgpt(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        req_body = json.loads(post_data.decode('utf-8'))

        user_message = req_body.get("message", "")

        if not user_message:
            self.send_json_response({"error": "Message is required"}, 400)
            return

        try:
            headers = {
                "Content-Type": "application/json",
                "api-key": AZURE_OPENAI_KEY
            }

            data = {
                "model": "gpt-4o-mini",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant. Keep responses short and direct."},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 2000,
                "temperature": 0.5
            }

            # Use the full Azure OpenAI endpoint URL
            azure_url = "https://txd61-m9nyyhgs-eastus2.cognitiveservices.azure.com/openai/deployments/gpt-4o-mini/chat/completions?api-version=2025-01-01-preview"
            response = requests.post(azure_url, json=data, headers=headers)
            response.raise_for_status()
            ai_response = response.json()

            if "choices" in ai_response and len(ai_response["choices"]) > 0:
                reply_text = ai_response["choices"][0]["message"]["content"]
            else:
                reply_text = "AI did not return a response."

            self.send_json_response({"reply": reply_text})

        except Exception as e:
            print(f"❌ ChatGPT API error: {str(e)}")
            import traceback
            traceback.print_exc()
            self.send_json_response({"error": "Azure AI request failed", "details": str(e)}, 500)

    def handle_deepseek(self):
        content_length = int(self.headers['Content-Length'])
        post_data = self.rfile.read(content_length)
        req_body = json.loads(post_data.decode('utf-8'))

        user_message = req_body.get("message", "")

        if not user_message:
            self.send_json_response({"error": "Message is required"}, 400)
            return

        try:
            url = f"{DEEPSEEK_ENDPOINT}/models/chat/completions?api-version=2024-05-01-preview"
            headers = {
                "Content-Type": "application/json",
                "api-key": AZURE_OPENAI_KEY
            }

            data = {
                "model": "DeepSeek-R1",
                "messages": [
                    {"role": "system", "content": "You are a helpful assistant. Keep responses short and direct."},
                    {"role": "user", "content": user_message}
                ],
                "max_tokens": 2000,
                "temperature": 0.7
            }

            response = requests.post(url, json=data, headers=headers)
            response.raise_for_status()
            ai_response = response.json()

            if "choices" in ai_response and len(ai_response["choices"]) > 0:
                full_response = ai_response["choices"][0]["message"]["content"]

                # Remove <think>...</think> from the response
                if "<think>" in full_response and "</think>" in full_response:
                    reply_text = full_response.split("</think>")[-1].strip()
                else:
                    reply_text = full_response
            else:
                reply_text = "AI did not return a response."

            self.send_json_response({"reply": reply_text})

        except Exception as e:
            print(f"❌ DeepSeek API error: {str(e)}")
            import traceback
            traceback.print_exc()
            self.send_json_response({"error": "Azure AI request failed", "details": str(e)}, 500)

    def send_json_response(self, data, status_code=200):
        self.send_response(status_code)
        self.send_header('Content-Type', 'application/json')
        self.send_header('Access-Control-Allow-Origin', '*')
        self.end_headers()
        self.wfile.write(json.dumps(data).encode('utf-8'))

def run_backend_server():
    PORT = 7071
    try:
        # Allow port reuse
        socketserver.TCPServer.allow_reuse_address = True
        with socketserver.TCPServer(("0.0.0.0", PORT), APIHandler) as httpd:
            print(f"🔥 Backend API server running at http://0.0.0.0:{PORT}")
            print("🤖 ChatGPT API: http://0.0.0.0:7071/api/ChatGpt_api")
            print("🧠 DeepSeek API: http://0.0.0.0:7071/api/DeepSeek_api")
            print("✅ Server ready to accept connections!")
            httpd.serve_forever()
    except OSError as e:
        if "Address already in use" in str(e):
            print(f"❌ Port {PORT} is already in use. Trying to kill existing process...")
            import subprocess
            try:
                subprocess.run(["pkill", "-f", "backend_server.py"], check=False)
                print("🔄 Retrying server startup...")
                import time
                time.sleep(2)
                with socketserver.TCPServer(("0.0.0.0", PORT), APIHandler) as httpd:
                    print(f"🔥 Backend API server running at http://0.0.0.0:{PORT}")
                    httpd.serve_forever()
            except Exception as retry_e:
                print(f"❌ Failed to restart server: {retry_e}")
                raise
        else:
            print(f"❌ Server startup error: {e}")
            raise

if __name__ == "__main__":
    print("🔧 Starting backend server...")
    print(f"🐍 Python version: {os.sys.version}")
    print(f"📁 Working directory: {os.getcwd()}")

    try:
        run_backend_server()
    except KeyboardInterrupt:
        print("\n👋 Backend server stopped by user")
    except Exception as e:
        print(f"❌ Backend server failed to start: {str(e)}")
        import traceback
        traceback.print_exc()
        import sys
        sys.exit(1)