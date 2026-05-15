import os

# MODE=LOCAL  → read config from app.yaml (local development)
# MODE=DBX    → read config from environment variables (Databricks Apps)
MODE: str = os.environ.get("MODE", "LOCAL")


def _load_yaml_env(yaml_path: str) -> dict:
    try:
        import yaml
    except ImportError:
        return {}
    if not os.path.isfile(yaml_path):
        return {}
    with open(yaml_path, encoding="utf-8") as f:
        data = yaml.safe_load(f)
    return {item["name"]: str(item["value"]) for item in data.get("env", [])}


if MODE == "LOCAL":
    _cfg = _load_yaml_env(
        os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "app.yaml")
    )

    def env(key: str, default: str = "") -> str:
        return _cfg.get(key, default)
else:
    def env(key: str, default: str = "") -> str:
        return os.environ.get(key, default)


DATABRICKS_HOST: str = env("DATABRICKS_HOST").rstrip("/")
WORKSPACE_ID: str = env("WORKSPACE_ID")

LAKEBASE_HOST: str = env("LAKEBASE_HOST")
LAKEBASE_PORT: int = int(env("LAKEBASE_PORT", "5432"))
LAKEBASE_DATABASE: str = env("LAKEBASE_DATABASE", "postgres")
LAKEBASE_USER: str = env("LAKEBASE_USER")
LAKEBASE_PASSWORD: str = env("LAKEBASE_PASSWORD")

PBI_TENANT_ID: str = env("PBI_TENANT_ID")
PBI_CLIENT_ID: str = env("PBI_CLIENT_ID")
PBI_CLIENT_SECRET: str = env("PBI_CLIENT_SECRET")

# space_code → (workspace_id, report_id, rls_role).
# rls_role = "" when the dataset has no Row-Level Security.
PBI_SPACES: dict[str, tuple[str, str, str]] = {
    "test_pl": (env("PBI_WORKSPACE_ID"), env("PBI_REPORT_ID"), ""),
    "asia_th_pos": (
        env("PBI_ASIA_TH_POS_WORKSPACE_ID"),
        env("PBI_ASIA_TH_POS_REPORT_ID"),
        env("PBI_ASIA_TH_POS_RLS_ROLE"),
    ),
}
