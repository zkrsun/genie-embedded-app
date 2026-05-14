from typing import List

from fastapi import APIRouter
from pydantic import BaseModel

from database import get_conn

router = APIRouter()


class CategoryOut(BaseModel):
    id: int
    name: str
    description: str | None = None


@router.get("/categories", response_model=List[CategoryOut])
def list_categories():
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                """
                SELECT id, name, description
                FROM opendata.categories
                ORDER BY id
                """
            )
            rows = cur.fetchall()
    return [CategoryOut(**row) for row in rows]
