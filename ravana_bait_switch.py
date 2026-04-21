import http.server
import socketserver
import threading

import config


_DECOY_HTML = b"""<!DOCTYPE html>
<html>
<head><meta charset="utf-8"><title>Home Dashboard</title></head>
<body style="font-family:sans-serif;margin:40px">
<h2>&#127968; Home Dashboard</h2>
<p>Status: <strong>Normal</strong></p>
<p>Uptime: 3d 14h 22m</p>
<p>Last sync: a few seconds ago</p>
<hr><small>Version 2.1.4 &mdash; Lily-Pi</small>
</body>
</html>"""


class _DecoyHandler(http.server.BaseHTTPRequestHandler):
    """Serve plausible-but-bogus HTML to any HTTP client."""

    def do_GET(self):  # noqa: N802
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.send_header("Content-Length", str(len(_DECOY_HTML)))
        self.end_headers()
        self.wfile.write(_DECOY_HTML)

    def log_message(self, format, *args):  # noqa: A002
        pass  # Suppress default access logging to stdout


class BaitSwitch:
    def __init__(self):
        self.mode = "SOVEREIGN"
        self._server = None
        self._thread = None

    def engage_decoy(self):
        self.mode = "DECOY"
        print("[RAVANA] 🎭 HEAD 16: DECOY MODE ACTIVE.")
        print("[HUD] Displaying fake desktop — hiding Lily-Pi node.")
        self._start_decoy_server()

    def _start_decoy_server(self):
        try:
            server = socketserver.TCPServer(("", config.DECOY_PORT), _DecoyHandler)
            server.allow_reuse_address = True
            self._server = server
            self._thread = threading.Thread(
                target=server.serve_forever, daemon=True, name="ravana-decoy"
            )
            self._thread.start()
            print(
                f"[RAVANA] 🌐 HEAD 16: Decoy HTTP server active on port {config.DECOY_PORT}."
            )
        except Exception as exc:
            print(f"[RAVANA] ⚠️  HEAD 16: Decoy server failed to start: {exc}")

    def stop_decoy(self):
        """Shut down the decoy HTTP server and return to SOVEREIGN mode."""
        if self._server:
            self._server.shutdown()
            self._server = None
            self._thread = None
        self.mode = "SOVEREIGN"
        print("[RAVANA] 🎭 HEAD 16: Decoy server stopped — mode SOVEREIGN.")


if __name__ == "__main__":
    switch = BaitSwitch()
    switch.engage_decoy()
    input("Press Enter to stop decoy server…")
    switch.stop_decoy()

