from typing import List

from fastapi import APIRouter, HTTPException

from config import DATABRICKS_HOST, WORKSPACE_ID
from database import get_conn
from models import BuOut, DomainOut, SpaceOut

router = APIRouter(prefix="/api")

_BUS_QUERY = """
    SELECT id, bu_name, bu_code, description
    FROM opendata.genie_bus
    WHERE is_active = 1
    ORDER BY display_order NULLS LAST, id
"""

_DOMAINS_QUERY = """
    SELECT id, bu_id, domain_name, domain_code, description
    FROM opendata.genie_domains
    WHERE is_active = 1
    ORDER BY display_order NULLS LAST, id
"""

_SPACES_QUERY = """
    SELECT bu_id, domain_id, space_name, space_code, space_key, description
    FROM opendata.genie_spaces
    WHERE is_active = 1
    ORDER BY display_order NULLS LAST, id
"""


def _genie_url(space_key: str) -> str:
    host = DATABRICKS_HOST
    if not host.startswith("http"):
        host = "https://" + host
    return f"{host}/embed/genie/rooms/{space_key}?o={WORKSPACE_ID}"


@router.get("/all", response_model=List[BuOut])
def get_all():
    """Full BU → Domain → Space hierarchy from lakebase."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(_BUS_QUERY)
            bus_rows = cur.fetchall()

            cur.execute(_DOMAINS_QUERY)
            domain_rows = cur.fetchall()

            cur.execute(_SPACES_QUERY)
            space_rows = cur.fetchall()

    # Index domains by id and group spaces into domains
    domains: dict = {
        row["id"]: {
            "bu_id": row["bu_id"],
            "name": row["domain_name"],
            "code": row["domain_code"],
            "description": row["description"],
            "spaces": [],
        }
        for row in domain_rows
    }

    for row in space_rows:
        domain = domains.get(row["domain_id"])
        if domain and row["space_key"]:
            domain["spaces"].append(
                SpaceOut(
                    name=row["space_name"],
                    code=row["space_code"],
                    url=_genie_url(row["space_key"]),
                    description=row["description"],
                )
            )

    return [
        BuOut(
            name=row["bu_name"],
            code=row["bu_code"],
            description=row["description"],
            domains=[
                DomainOut(
                    name=d["name"],
                    code=d["code"],
                    description=d["description"],
                    spaces=d["spaces"],
                )
                for d in domains.values()
                if d["bu_id"] == row["id"]
            ],
        )
        for row in bus_rows
    ]


@router.get("/bus")
def get_bus():
    """List all active BUs."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(_BUS_QUERY)
            rows = cur.fetchall()
    return [{"name": r["bu_name"], "code": r["bu_code"]} for r in rows]


@router.get("/domains/{bu_code}")
def get_domains(bu_code: str):
    """List domains for a given BU code."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT d.domain_name, d.domain_code, d.description
                FROM opendata.genie_domains d
                JOIN opendata.genie_bus b ON b.id = d.bu_id
                WHERE b.bu_code = %s AND d.is_active = 1 AND b.is_active = 1
                ORDER BY d.display_order NULLS LAST, d.id
                """,
                (bu_code,),
            )
            rows = cur.fetchall()
    if not rows:
        raise HTTPException(status_code=404, detail=f"BU '{bu_code}' not found or has no active domains")
    return [{"name": r["domain_name"], "code": r["domain_code"], "description": r["description"]} for r in rows]


@router.get("/spaces/{bu_code}/{domain_code}")
def get_spaces(bu_code: str, domain_code: str):
    """List genie spaces for a given BU and domain."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT s.space_name, s.space_code, s.space_key, s.description
                FROM opendata.genie_spaces s
                JOIN opendata.genie_domains d ON d.id = s.domain_id
                JOIN opendata.genie_bus b ON b.id = s.bu_id
                WHERE b.bu_code = %s AND d.domain_code = %s
                  AND s.is_active = 1 AND d.is_active = 1 AND b.is_active = 1
                ORDER BY s.display_order NULLS LAST, s.id
                """,
                (bu_code, domain_code),
            )
            rows = cur.fetchall()
    if not rows:
        raise HTTPException(
            status_code=404,
            detail=f"No active spaces found for BU '{bu_code}' / domain '{domain_code}'",
        )
    return [
        {
            "name": r["space_name"],
            "code": r["space_code"],
            "url": _genie_url(r["space_key"]),
            "description": r["description"],
        }
        for r in rows
        if r["space_key"]
    ]
