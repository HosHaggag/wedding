#!/usr/bin/env python3
"""Serve the scraped wedding card site locally."""
import http.server
import socketserver
from pathlib import Path

PORT = 8765
ROOT = Path(__file__).resolve().parent / "wedding.fadl.info"


class Handler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        super().__init__(*args, directory=str(ROOT), **kwargs)

    extensions_map = {
        **http.server.SimpleHTTPRequestHandler.extensions_map,
        ".js": "application/javascript",
        ".mjs": "application/javascript",
        ".css": "text/css",
        ".webp": "image/webp",
        ".svg": "image/svg+xml",
        ".woff2": "font/woff2",
        ".webmanifest": "application/manifest+json",
    }


def main():
    if not ROOT.is_dir():
        raise SystemExit(f"Missing site folder: {ROOT}")
    with socketserver.TCPServer(("0.0.0.0", PORT), Handler) as httpd:
        httpd.allow_reuse_address = True
        print(f"Serving {ROOT} at http://localhost:{PORT}/  (Ctrl+C to stop)")
        try:
            httpd.serve_forever()
        except KeyboardInterrupt:
            print("\nStopped.")


if __name__ == "__main__":
    main()
