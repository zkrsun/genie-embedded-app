from typing import List

from fastapi import APIRouter, HTTPException, Request, Response
from pydantic import BaseModel

from auth import user_email as _user_email_helper
from config import DATABRICKS_HOST, WORKSPACE_ID
from database import get_conn
from models import SpaceOut
from pbi_service import get_embed_params as _get_pbi_embed_params

router = APIRouter(prefix="/api")

_SPACES_QUERY = """
    SELECT
        s.space_name,
        s.space_code,
        s.space_key,
        s.description,
        s.icon_code,
        COALESCE(l.access_count, 0) AS access_count
    FROM opendata.genie_spaces s
    LEFT JOIN (
        SELECT space_code, COUNT(*) AS access_count
        FROM opendata.genie_access_log
        WHERE accessed_at >= now() - INTERVAL '30 days'
        GROUP BY space_code
    ) l ON l.space_code = s.space_code
    WHERE s.is_active = 1
    ORDER BY s.display_order NULLS LAST, s.id
"""


def _genie_url(space_key: str) -> str:
    host = DATABRICKS_HOST
    if not host.startswith("http"):
        host = "https://" + host
    return f"{host}/embed/genie/rooms/{space_key}?o={WORKSPACE_ID}"


def _user_email(request: Request) -> str:
    return _user_email_helper(request)


@router.get("/all", response_model=List[SpaceOut])
def get_all():
    """Flat list of active Genie spaces from lakebase."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(_SPACES_QUERY)
            rows = cur.fetchall()

    return [
        SpaceOut(
            name=row["space_name"],
            code=row["space_code"],
            url=_genie_url(row["space_key"]),
            description=row["description"],
            icon_code=row["icon_code"],
            access_count=row["access_count"],
        )
        for row in rows
        if row["space_key"]
    ]


class SpaceAccessIn(BaseModel):
    space_code: str


@router.post("/log/space-access", status_code=204)
def log_space_access(payload: SpaceAccessIn, request: Request) -> Response:
    """Record that a user opened a Genie space (called by GenieView on mount)."""
    user_email = _user_email(request)
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "INSERT INTO opendata.genie_access_log (user_email, space_code) VALUES (%s, %s)",
                (user_email, payload.space_code),
            )
        conn.commit()
    return Response(status_code=204)


@router.get("/pbi/embed")
def get_pbi_embed(space: str):
    """Return PowerBI embed params for the given Genie space."""
    try:
        return _get_pbi_embed_params(space)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc))
