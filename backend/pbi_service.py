"""
Minimal PowerBI embed helper for the test_pl Genie page.

Acquires a Service Principal access token via MSAL, then asks the PowerBI
REST API for a single-report embed token. Returns `accessToken` + `embedUrl`
ready to be consumed by the powerbi-client JS SDK.
"""
import json
from typing import Optional

import requests
from msal import ConfidentialClientApplication

from config import (
    PBI_TENANT_ID,
    PBI_CLIENT_ID,
    PBI_CLIENT_SECRET,
    PBI_WORKSPACE_ID,
    PBI_REPORT_ID,
)

_SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]


def _missing_config() -> Optional[str]:
    required = {
        "PBI_TENANT_ID": PBI_TENANT_ID,
        "PBI_CLIENT_ID": PBI_CLIENT_ID,
        "PBI_CLIENT_SECRET": PBI_CLIENT_SECRET,
        "PBI_WORKSPACE_ID": PBI_WORKSPACE_ID,
        "PBI_REPORT_ID": PBI_REPORT_ID,
    }
    missing = [k for k, v in required.items() if not v]
    if missing:
        return "Missing PowerBI config: " + ", ".join(missing)
    return None


def _get_access_token() -> str:
    app = ConfidentialClientApplication(
        client_id=PBI_CLIENT_ID,
        client_credential=PBI_CLIENT_SECRET,
        authority=f"https://login.microsoftonline.com/{PBI_TENANT_ID}",
    )
    result = app.acquire_token_for_client(scopes=_SCOPE)
    if "access_token" not in result:
        raise RuntimeError(
            f"Failed to acquire PowerBI token: {result.get('error')} - {result.get('error_description')}"
        )
    return result["access_token"]


def _auth_headers(token: str) -> dict:
    return {"Authorization": f"Bearer {token}", "Content-Type": "application/json"}


def get_embed_params() -> dict:
    """Return { accessToken, embedUrl, reportId } for the configured PBI report."""
    err = _missing_config()
    if err:
        raise RuntimeError(err)

    access_token = _get_access_token()

    report_resp = requests.get(
        f"https://api.powerbi.com/v1.0/myorg/groups/{PBI_WORKSPACE_ID}/reports/{PBI_REPORT_ID}",
        headers=_auth_headers(access_token),
        timeout=30,
    )
    if report_resp.status_code != 200:
        raise RuntimeError(
            f"PowerBI report lookup failed ({report_resp.status_code}): {report_resp.text}"
        )
    report = report_resp.json()
    embed_url = report["embedUrl"]
    dataset_id = report.get("datasetId")

    body = {
        "datasets": [{"id": dataset_id}] if dataset_id else [],
        "reports": [{"id": PBI_REPORT_ID}],
        "targetWorkspaces": [{"id": PBI_WORKSPACE_ID}],
    }
    token_resp = requests.post(
        "https://api.powerbi.com/v1.0/myorg/GenerateToken",
        headers=_auth_headers(access_token),
        data=json.dumps(body),
        timeout=30,
    )
    if token_resp.status_code != 200:
        raise RuntimeError(
            f"PowerBI embed token generation failed ({token_resp.status_code}): {token_resp.text}"
        )
    embed_token = token_resp.json()["token"]

    return {
        "accessToken": embed_token,
        "embedUrl": embed_url,
        "reportId": PBI_REPORT_ID,
    }
