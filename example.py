#!/usr/bin/env python3
"""
Databricks Genie Embedded Space - Example Server
Reference: https://docs.databricks.com/aws/en/genie/embed

Prerequisites (must be done in Databricks before this will work):
  1. Enable the "Embed Genie spaces" feature preview in your workspace.
  2. Open the Genie space → Share → Embed space → add this server's
     origin (e.g. http://localhost:3000) to the allowed embedding surfaces.
  3. Users must have access to both the Genie space and the underlying data.
"""

import os
import sys
from http.server import HTTPServer, BaseHTTPRequestHandler

try:
    import yaml
    _HAS_YAML = True
except ImportError:
    _HAS_YAML = False

# -----------------------------------------------------------------------------
# Config  (environment variables take priority; app.yaml used as fallback)
# -----------------------------------------------------------------------------
def _load_yaml_config(yaml_path="app.yaml"):
    if not _HAS_YAML or not os.path.exists(yaml_path):
        return {}
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return {item["name"]: str(item["value"]) for item in data.get("env", [])}

_yaml = _load_yaml_config()

def _get(key, default=None):
    return os.environ.get(key) or _yaml.get(key) or default

CONFIG = {
    "databricks_host": _get("DATABRICKS_HOST"),
    "genie_space_id":  _get("GENIE_SPACE_ID"),
    "workspace_id":    _get("WORKSPACE_ID"),
    "port":            int(_get("PORT", 3000)),
}

# -----------------------------------------------------------------------------
# HTML generator
# -----------------------------------------------------------------------------
def generate_html():
    host = CONFIG["databricks_host"].rstrip("/")
    if not host.startswith("http"):
        host = "https://" + host

    # URL format: /embed/genie/rooms/<space-id>?o=<workspace-id>
    # Obtain this URL via: Genie space → Share → Embed space → copy iframe src
    genie_url = f"{host}/embed/genie/rooms/{CONFIG['genie_space_id']}?o={CONFIG['workspace_id']}"

    return f"""<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Genie</title>
    <style>
        * {{ margin: 0; padding: 0; box-sizing: border-box; }}
        body {{ height: 100vh; overflow: hidden; }}
        iframe {{
            width: 100%;
            height: 100vh;
            border: none;
            display: block;
        }}
    </style>
</head>
<body>
    <!--
        Embed a Databricks Genie space as an iframe.
        - allow="clipboard-write" enables copying CSV data and conversation links.
        - Users who are not signed in to Databricks will be prompted to authenticate.
        - Embedded users can send prompts but cannot edit the space configuration.
        Reference: https://docs.databricks.com/aws/en/genie/embed
    -->
    <iframe
        src="{genie_url}"
        allow="clipboard-write"
        width="100%"
        height="600"
        frameborder="0"
    ></iframe>
</body>
</html>"""

# -----------------------------------------------------------------------------
# HTTP server
# -----------------------------------------------------------------------------
class RequestHandler(BaseHTTPRequestHandler):
    def do_GET(self):
        if self.path != "/":
            self.send_response(404)
            self.send_header("Content-Type", "text/plain")
            self.end_headers()
            self.wfile.write(b"Not Found")
            return

        html = generate_html()
        self.send_response(200)
        self.send_header("Content-Type", "text/html; charset=utf-8")
        self.end_headers()
        self.wfile.write(html.encode())

    def log_message(self, *_):
        pass  # suppress request logs


def start_server():
    if not CONFIG["databricks_host"]:
        print("Missing: DATABRICKS_HOST", file=sys.stderr)
        sys.exit(1)

    host = CONFIG["databricks_host"].rstrip("/")
    space_id = CONFIG["genie_space_id"]
    workspace_id = CONFIG["workspace_id"]
    port = CONFIG["port"]

    server = HTTPServer(("0.0.0.0", port), RequestHandler)
    print(f"Server running at:  http://localhost:{port}")
    print(f"Embedding Genie space: {host}/embed/genie/rooms/{space_id}?o={workspace_id}")
    print()
    print("Remember to add http://localhost:{} to the allowed embedding".format(port))
    print("surfaces in your Genie space settings (Share → Embed space).")
    try:
        server.serve_forever()
    except KeyboardInterrupt:
        sys.exit(0)


if __name__ == "__main__":
    start_server()
