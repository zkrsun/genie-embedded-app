"""
Minimal PowerBI embed helper for Genie pages.

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
    PBI_SPACES,
)

_SCOPE = ["https://analysis.windows.net/powerbi/api/.default"]


def _missing_credentials() -> Optional[str]:
    creds = {
        "PBI_TENANT_ID": PBI_TENANT_ID,
        "PBI_CLIENT_ID": PBI_CLIENT_ID,
        "PBI_CLIENT_SECRET": PBI_CLIENT_SECRET,
    }
    missing = [k for k, v in creds.items() if not v]
    if missing:
        return "Missing PowerBI credentials: " + ", ".join(missing)
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


def get_embed_params(space_code: str) -> dict:
    """Return { accessToken, embedUrl, reportId } for the given space's PBI report."""
    err = _missing_credentials()
    if err:
        raise RuntimeError(err)

    if space_code not in PBI_SPACES:
        raise RuntimeError(f"No PowerBI report configured for space '{space_code}'")

    workspace_id, report_id, rls_role = PBI_SPACES[space_code]
    if not workspace_id or not report_id:
        raise RuntimeError(
            f"Missing workspace_id or report_id in app.yaml for space '{space_code}'"
        )

    access_token = _get_access_token()

    report_resp = requests.get(
        f"https://api.powerbi.com/v1.0/myorg/groups/{workspace_id}/reports/{report_id}",
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
        "reports": [{"id": report_id}],
        "targetWorkspaces": [{"id": workspace_id}],
    }

    # When the dataset has RLS, PowerBI requires an effective identity.
    # Using the Service Principal's CLIENT_ID as the username + the configured role.
    if rls_role:
        if not dataset_id:
            raise RuntimeError(
                f"Cannot apply RLS for space '{space_code}': report has no associated dataset"
            )
        body["identities"] = [
            {
                "username": PBI_CLIENT_ID,
                "roles": [rls_role],
                "datasets": [dataset_id],
            }
        ]
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
        "reportId": report_id,
    }
