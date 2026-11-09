"""Calculator GPT - Standalone Desktop Application & Local Python Engine.
Runs as a native Windows desktop app via pywebview with an embedded HTTP server
and advanced offline CAS & mathematical reasoning engine.
"""

import os
import sys
import json
import socket
import threading
from http.server import SimpleHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs, urlparse

import webview
from engine.master_solver import process_all_queries, solve_query
from engine.llm_engine import preload_llm_async

if getattr(sys, 'frozen', False):
    BASE_DIR = getattr(sys, '_MEIPASS', os.path.dirname(sys.executable))
else:
    BASE_DIR = os.path.dirname(os.path.abspath(__file__))

PORT = 8765


class CalculatorApi:
    """Exposed directly to JavaScript inside the desktop app window."""

    def solve(self, query: str) -> str:
        """Solves a single or multi-part mathematical query and returns JSON."""
        try:
            results = process_all_queries(query)
            return json.dumps({"status": "success", "results": results})
        except Exception as e:
            return json.dumps({
                "status": "error",
                "message": str(e),
                "results": [{
                    "title": "Computation Error",
                    "summary_value": "Error executing calculation",
                    "formula": "",
                    "rows": [["Error Details", str(e)]],
                    "steps": ["An error occurred while evaluating the mathematical expression."],
                    "insights": "Please check syntax or try rephrasing."
                }]
            })

    def get_system_status(self) -> str:
        """Returns engine status and installed modules."""
        import sympy
        return json.dumps({
            "engine": "Python SymPy CAS & Quantitative Aptitude",
            "version": "2.5 Pro Standalone",
            "sympy_version": sympy.__version__,
            "status": "operational",
            "offline": True
        })


class ApiRequestHandler(SimpleHTTPRequestHandler):
    """Serves the static glassmorphic frontend and handles /api/solve requests."""

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=BASE_DIR, **kwargs)

    def end_headers(self):
        self.send_header('Cache-Control', 'no-cache, no-store, must-revalidate')
        self.send_header('Pragma', 'no-cache')
        self.send_header('Expires', '0')
        super().end_headers()

    def do_POST(self):
        if self.path == '/api/solve':
            content_length = int(self.headers.get('Content-Length', 0))
            post_data = self.rfile.read(content_length).decode('utf-8')
            try:
                body = json.loads(post_data)
                query = body.get('q', '')
                results = process_all_queries(query)
                response = json.dumps({"status": "success", "results": results}, separators=(',', ':'))
            except Exception as e:
                response = json.dumps({"status": "error", "message": str(e), "results": []})

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        else:
            self.send_error(404, "Not Found")

    def do_GET(self):
        parsed = urlparse(self.path)
        if parsed.path == '/api/solve':
            params = parse_qs(parsed.query)
            query = params.get('q', [''])[0]
            try:
                results = process_all_queries(query)
                response = json.dumps({"status": "success", "results": results}, separators=(',', ':'))
            except Exception as e:
                response = json.dumps({"status": "error", "message": str(e), "results": []})

            self.send_response(200)
            self.send_header('Content-Type', 'application/json; charset=utf-8')
            self.send_header('Access-Control-Allow-Origin', '*')
            self.end_headers()
            self.wfile.write(response.encode('utf-8'))
        else:
            super().do_GET()

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header('Access-Control-Allow-Origin', '*')
        self.send_header('Access-Control-Allow-Methods', 'GET, POST, OPTIONS')
        self.send_header('Access-Control-Allow-Headers', 'Content-Type')
        self.end_headers()

    def log_message(self, format, *args):
        # Suppress noisy HTTP request logging
        pass


def is_port_in_use(port: int) -> bool:
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        return s.connect_ex(('127.0.0.1', port)) == 0


def start_server():
    """Runs internal daemon web server with dynamic fallback if default port is occupied."""
    global PORT
    for p in range(8765, 8780):
        try:
            server = ThreadingHTTPServer(('127.0.0.1', p), ApiRequestHandler)
            PORT = p
            t = threading.Thread(target=server.serve_forever, daemon=True)
            t.start()
            print(f"[*] Local Calculator GPT HTTP Service running on http://127.0.0.1:{PORT}")
            return PORT
        except OSError:
            if is_port_in_use(p):
                PORT = p
                print(f"[*] Reusing active local service on port {PORT}")
                return PORT
            continue
    return PORT


def main():
    start_server()
    preload_llm_async()
    api = CalculatorApi()

    # If --server flag is passed, just keep serving HTTP
    if '--server' in sys.argv:
        print(f"[*] Server mode active at http://127.0.0.1:{PORT}. Press Ctrl+C to stop.")
        try:
            import time
            while True:
                time.sleep(1)
        except KeyboardInterrupt:
            print("\nShutting down.")
            return

    # Native Desktop Application Window via pywebview
    url = f"http://127.0.0.1:{PORT}/index.html"
    print("[*] Launching Calculator GPT Standalone Desktop App Window...")

    window = webview.create_window(
        title="Calculator GPT",
        url=url,
        js_api=api,
        width=350,
        height=580,
        min_size=(320, 500),
        background_color='#05060b',
        text_select=True
    )

    webview.start(debug=False)


if __name__ == '__main__':
    main()
