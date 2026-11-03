import os
import sys
import json
import http.server
import socketserver
import webbrowser
from typing import Dict, Any

if hasattr(sys.stdout, "reconfigure"):
    sys.stdout.reconfigure(encoding="utf-8", errors="replace")
    sys.stderr.reconfigure(encoding="utf-8", errors="replace")

DASHBOARD_DIR = os.path.dirname(os.path.abspath(__file__))

class CyberDeckHandler(http.server.SimpleHTTPRequestHandler):
    """
    Custom HTTP request handler serving the CyberDeck 3D interface and REST API.
    """

    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DASHBOARD_DIR, **kwargs)

    def end_headers(self):
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        self.send_header("Pragma", "no-cache")
        self.send_header("Expires", "0")
        super().end_headers()

    def do_GET(self):
        if self.path == "/api/status":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            status_data = {
                "status": "OPERATIONAL",
                "active_incidents": 0,
                "mtta_seconds": 12,
                "mttr_seconds": 171,
                "services": [
                    {"name": "checkout-service", "status": "HEALTHY", "latency_ms": 18.4},
                    {"name": "payment-gateway", "status": "HEALTHY", "latency_ms": 24.1},
                    {"name": "postgres-primary", "status": "HEALTHY", "latency_ms": 4.2},
                    {"name": "redis-cache", "status": "HEALTHY", "latency_ms": 1.1}
                ]
            }
            self.wfile.write(json.dumps(status_data).encode("utf-8"))
        elif self.path == "/api/simulate":
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            res = {
                "incident_id": "INC-502",
                "severity": "P0",
                "service": "checkout-service",
                "error": "ZeroDivisionError",
                "resolved": True,
                "duration_seconds": 171,
                "approver": "@Shubham"
            }
            self.wfile.write(json.dumps(res).encode("utf-8"))
        else:
            super().do_GET()

def start_server(port: int = 8080, open_browser: bool = True):
    server_class = getattr(http.server, "ThreadingHTTPServer", socketserver.TCPServer)
    with server_class(("", port), CyberDeckHandler) as httpd:
        url = f"http://localhost:{port}"
        print(f"============================================================")
        print(f"[+] SwitchGuard CyberDeck Dashboard Live at {url}")
        print(f"============================================================")
        if open_browser:
            webbrowser.open(url)
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nShutting down CyberDeck dashboard server.")

if __name__ == "__main__":
    start_server(port=8080, open_browser=True)
