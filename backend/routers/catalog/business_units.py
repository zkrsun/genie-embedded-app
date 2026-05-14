import os
from typing import List, Optional

from fastapi import APIRouter
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel

from database import get_conn

router = APIRouter()

# Logos live in <repo-root>/logos/*.svg — siblings of backend/ and frontend/.
LOGOS_DIR = os.path.realpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "..", "..", "logos")
)


class BusinessUnitOut(BaseModel):
    id: int
    name: str
    code: str
    logo_filename: Optional[str] = None
    display_order: int = 0
    is_active: int = 1
    api_calls: int = 0
    download_count: int = 0


@router.get("/business-units", response_model=List[BusinessUnitOut])
def list_business_units():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, code, logo_filename, display_order,
                       is_active, api_calls, download_count
                FROM opendata.business_units
                WHERE is_active = 1
                ORDER BY display_order ASC, id ASC
                """
            )
            rows = cur.fetchall()
    return [BusinessUnitOut(**row) for row in rows]


@router.get("/business-units/{bu_id}/logo")
def get_business_unit_logo(bu_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT logo_filename FROM opendata.business_units WHERE id = %s",
                (bu_id,),
            )
            row = cur.fetchone()

    if not row or not row["logo_filename"]:
        return JSONResponse({"error": "Logo not found"}, status_code=404)

    logo_path = os.path.realpath(os.path.join(LOGOS_DIR, row["logo_filename"]))
    if not logo_path.startswith(LOGOS_DIR) or not os.path.isfile(logo_path):
        return JSONResponse({"error": "Logo file not found"}, status_code=404)
    return FileResponse(logo_path, media_type="image/svg+xml")
