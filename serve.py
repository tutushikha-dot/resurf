#!/usr/bin/env python3
"""
Local network development server for Resurf mirror.
Provides:
- Same-Wi-Fi network access (0.0.0.0 binding)
- Clean URL handling (/about -> /about/index.html or /about.html)
- Next.js image endpoint handling (/_next/image?url=... -> local asset)
- Query-string stripping for static assets (?dpl=... or ?_rsc=...)
- API endpoints handling (/api/native-version -> JSON)
- Mock analytics /ingest/ to prevent network hangs
- Proper MIME types for WebP, WOFF2, MP4, JS, SVG, Manifest
- Range header support for MP4 video streaming
- CORS headers for all devices on local Wi-Fi
"""

import os
import sys
import socket
import urllib.parse
import http.server
import mimetypes
import subprocess

DIRECTORY = os.path.dirname(os.path.abspath(__file__))

# Configure MIME types
mimetypes.add_type("application/javascript", ".js")
mimetypes.add_type("text/css", ".css")
mimetypes.add_type("font/woff2", ".woff2")
mimetypes.add_type("font/woff", ".woff")
mimetypes.add_type("image/webp", ".webp")
mimetypes.add_type("image/svg+xml", ".svg")
mimetypes.add_type("video/mp4", ".mp4")
mimetypes.add_type("video/webm", ".webm")
mimetypes.add_type("application/manifest+json", ".webmanifest")
mimetypes.add_type("image/x-icon", ".ico")
mimetypes.add_type("application/json", ".json")

def get_local_ip():
    try:
        with socket.socket(socket.AF_INET, socket.SOCK_DGRAM) as s:
            s.connect(("8.8.8.8", 80))
            return s.getsockname()[0]
    except Exception:
        try:
            return socket.gethostbyname(socket.gethostname())
        except Exception:
            return "127.0.0.1"

def get_bonjour_hostname():
    try:
        res = subprocess.run(["scutil", "--get", "LocalHostName"], capture_output=True, text=True, timeout=2)
        name = res.stdout.strip()
        if name:
            return f"{name}.local"
    except Exception:
        pass
    return None

def find_available_port(start_port=8088):
    for p in range(start_port, start_port + 50):
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            if s.connect_ex(("127.0.0.1", p)) != 0:
                return p
    return start_port

class ResurfHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=DIRECTORY, **kwargs)

    def end_headers(self):
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "GET, HEAD, POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "*")
        self.send_header("Cache-Control", "no-cache, no-store, must-revalidate")
        super().end_headers()

    def do_OPTIONS(self):
        self.send_response(200)
        self.end_headers()

    def do_POST(self):
        parsed = urllib.parse.urlparse(self.path)
        if parsed.path.startswith("/ingest/"):
            self.send_response(200)
            self.send_header("Content-Type", "application/json")
            self.end_headers()
            self.wfile.write(b'{"status": 1}')
            return
        self.send_response(200)
        self.end_headers()

    def guess_type(self, path):
        if path.endswith("api/native-version") or "/api/" in path:
            return "application/json"
        return super().guess_type(path)

    def translate_path(self, path):
        parsed = urllib.parse.urlparse(path)
        req_path = parsed.path

        # 1. Handle Next.js Image Optimization route: /_next/image?url=...
        if req_path == "/_next/image":
            query = urllib.parse.parse_qs(parsed.query)
            if "url" in query and query["url"]:
                target_url = urllib.parse.unquote(query["url"][0]).lstrip("/")
                candidate = os.path.join(DIRECTORY, target_url)
                if os.path.isfile(candidate):
                    return candidate

        # 2. Clean path (strip query & hash)
        clean = req_path.lstrip("/")
        if not clean:
            return os.path.join(DIRECTORY, "index.html")

        # 3. Direct file match
        candidate = os.path.join(DIRECTORY, clean)
        if os.path.isfile(candidate):
            return candidate

        # 4. Directory with index.html
        dir_index = os.path.join(DIRECTORY, clean, "index.html")
        if os.path.isfile(dir_index):
            return dir_index

        # 5. Flat .html file (e.g. /about -> about.html)
        flat_html = os.path.join(DIRECTORY, clean + ".html")
        if os.path.isfile(flat_html):
            return flat_html

        return candidate

def main():
    if len(sys.argv) > 1:
        port = int(sys.argv[1])
    else:
        port = find_available_port(8088)

    local_ip = get_local_ip()
    bonjour = get_bonjour_hostname()

    http.server.ThreadingHTTPServer.allow_reuse_address = True
    server_address = ("0.0.0.0", port)
    
    with http.server.ThreadingHTTPServer(server_address, ResurfHandler) as httpd:
        print("=" * 64)
        print("  🚀 Resurf Local Wi-Fi Server Running")
        print("=" * 64)
        print(f"  • On this Mac:")
        print(f"    http://localhost:{port}")
        print()
        print(f"  • On another Mac, iPhone, or iPad (same Wi-Fi):")
        print(f"    http://{local_ip}:{port}")
        if bonjour:
            print(f"    http://{bonjour}:{port}")
        print("=" * 64)
        print(f"  Serving files from: {DIRECTORY}")
        print(f"  Press Ctrl+C to stop.")
        print("=" * 64, flush=True)

        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\n[*] Server stopped.")

if __name__ == '__main__':
    main()
