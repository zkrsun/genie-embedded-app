from typing import Any, List, Optional

from fastapi import APIRouter, HTTPException
from pydantic import BaseModel

from database import get_conn

router = APIRouter()


class CategoryNested(BaseModel):
    id: int
    name: str
    description: Optional[str] = None


class DatasetOut(BaseModel):
    id: int
    title: str
    description: str
    category_id: int
    tags: Optional[str] = None
    row_count: int = 0
    col_count: int = 0
    download_count: int = 0
    created_at: str
    updated_at: str
    category: CategoryNested
    # JSON column from opendata.datasets — array of {name, type, description}
    column_descriptions: Optional[List[Any]] = None


def _row_to_dataset(row: dict) -> DatasetOut:
    return DatasetOut(
        id=row["id"],
        title=row["title"],
        description=row["description"] or "",
        category_id=row["category_id"],
        tags=row["tags"],
        row_count=row["row_count"] or 0,
        col_count=row["col_count"] or 0,
        download_count=row["download_count"] or 0,
        created_at=row["created_at"].isoformat() if row["created_at"] else "",
        updated_at=row["updated_at"].isoformat() if row["updated_at"] else "",
        category=CategoryNested(
            id=row["cat_id"],
            name=row["cat_name"],
            description=row["cat_description"],
        ),
        column_descriptions=row["column_descriptions"],
    )


_BASE_SELECT = """
    SELECT
        d.id, d.title, d.description, d.category_id, d.tags,
        d.row_count, d.col_count, d.download_count,
        d.created_at, d.updated_at, d.column_descriptions,
        c.id AS cat_id, c.name AS cat_name, c.description AS cat_description
    FROM opendata.datasets d
    JOIN opendata.categories c ON c.id = d.category_id
"""


@router.get("/datasets/popular", response_model=List[DatasetOut])
def get_popular(limit: int = 10):
    """Datasets ordered by download_count desc."""
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                _BASE_SELECT + " ORDER BY d.download_count DESC NULLS LAST LIMIT %s",
                (limit,),
            )
            rows = cur.fetchall()
    return [_row_to_dataset(r) for r in rows]


@router.get("/datasets/{dataset_id}", response_model=DatasetOut)
def get_dataset(dataset_id: int):
    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(_BASE_SELECT + " WHERE d.id = %s", (dataset_id,))
            row = cur.fetchone()
    if not row:
        raise HTTPException(status_code=404, detail="Dataset not found")
    return _row_to_dataset(row)
