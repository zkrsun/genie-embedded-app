import os
from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
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

# Allow Vite dev server to call the API in local development
if MODE == "LOCAL":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["GET"],
        allow_headers=["*"],
    )

DATABRICKS_HOST = _env("DATABRICKS_HOST").rstrip("/")
WORKSPACE_ID    = _env("WORKSPACE_ID")

SPACES = [
    {"bu": "SBFGHQ", "spaces": [
        {"name": "RMS",     "id": _env("GENIE_SPACE_RMS")},
        {"name": "SELLIN",  "id": _env("GENIE_SPACE_SELLIN")},
        {"name": "SELLOUT", "id": _env("GENIE_SPACE_SELLOUT")},
        {"name": "MACRO",   "id": _env("GENIE_SPACE_MACRO")},
    ]},
    {"bu": "SBFA", "spaces": [
        {"name": "MACRO",   "id": _env("GENIE_SPACE_MACRO")},
    ]},
]

# Pre-build a lookup dict for O(1) BU access
_BU_INDEX: dict = {entry["bu"]: entry for entry in SPACES}


def _genie_url(space_id: str) -> str:
    host = DATABRICKS_HOST
    if not host.startswith("http"):
        host = "https://" + host
    return f"{host}/embed/genie/rooms/{space_id}?o={WORKSPACE_ID}"


def _serialise_spaces(spaces: list) -> list:
    return [
        {"name": s["name"], "url": _genie_url(s["id"])}
        for s in spaces
        if s["id"]
    ]


@app.get("/api/all")
def get_all():
    """All BUs with their spaces — single request for frontend initialisation."""
    return [
        {"bu": entry["bu"], "spaces": _serialise_spaces(entry["spaces"])}
        for entry in SPACES
    ]


@app.get("/api/bu_s")
def get_bu_s():
    return [entry["bu"] for entry in SPACES]


@app.get("/api/spaces/{bu}")
def get_spaces_by_bu(bu: str):
    entry = _BU_INDEX.get(bu)
    if entry is None:
        raise HTTPException(status_code=404, detail=f"BU '{bu}' not found")
    return _serialise_spaces(entry["spaces"])


# Serve Vue built static files — must be mounted last
_dist = os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "dist")
if os.path.isdir(_dist):
    app.mount("/", StaticFiles(directory=_dist, html=True), name="static")
