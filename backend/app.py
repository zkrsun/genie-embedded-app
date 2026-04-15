import os
from fastapi import FastAPI
from fastapi.staticfiles import StaticFiles

# MODE=LOCAL  → read config from app.yaml (local development)
# MODE=DBX    → read config from environment variables (Databricks Apps)
MODE = os.environ.get("MODE", "LOCAL")


def _load_yaml_env(yaml_path: str) -> dict:
    try:
        import yaml
    except ImportError:
        return {}
    if not os.path.isfile(yaml_path):
        return {}
    with open(yaml_path) as f:
        data = yaml.safe_load(f)
    return {item["name"]: str(item["value"]) for item in data.get("env", [])}


if MODE == "LOCAL":
    _cfg = _load_yaml_env(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app.yaml")
    )
    def _env(key: str, default: str = "") -> str:
        return _cfg.get(key, default)
else:
    def _env(key: str, default: str = "") -> str:
        return os.environ.get(key, default)


app = FastAPI()

DATABRICKS_HOST = _env("DATABRICKS_HOST").rstrip("/")
WORKSPACE_ID    = _env("WORKSPACE_ID")

SPACES = [
    {"name": "RMS",     "id": _env("GENIE_SPACE_RMS")},
    {"name": "SELLIN",  "id": _env("GENIE_SPACE_SELLIN")},
    {"name": "SELLOUT", "id": _env("GENIE_SPACE_SELLOUT")},
]


def _genie_url(space_id: str) -> str:
    host = DATABRICKS_HOST
    if not host.startswith("http"):
        host = "https://" + host
    return f"{host}/embed/genie/rooms/{space_id}?o={WORKSPACE_ID}"


@app.get("/api/spaces")
def get_spaces():
    return [
        {"name": s["name"], "url": _genie_url(s["id"])}
        for s in SPACES
        if s["id"]
    ]


# Serve Vue built static files — must be mounted last
_dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "dist")
if os.path.isdir(_dist):
    app.mount("/", StaticFiles(directory=_dist, html=True), name="static")
