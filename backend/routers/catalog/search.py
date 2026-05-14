from typing import List, Optional

from fastapi import APIRouter, Query
from pydantic import BaseModel

from database import get_conn

from .datasets import DatasetOut, _BASE_SELECT, _row_to_dataset

router = APIRouter()


class SearchResult(BaseModel):
    total: int
    datasets: List[DatasetOut]


def _build_text_clause(query: str) -> tuple[str, list]:
    """Build WHERE clause + params for a multi-keyword search with AND→OR fallback.

    Returns (sql_fragment, params). sql_fragment includes a leading 'AND' if non-empty.
    """
    keywords = query.strip().split()
    if not keywords:
        return "", []

    def _kw_clauses(op: str) -> tuple[str, list]:
        parts = []
        params: list = []
        for kw in keywords:
            parts.append("(d.title ILIKE %s OR d.description ILIKE %s OR d.tags ILIKE %s)")
            like = f"%{kw}%"
            params.extend([like, like, like])
        return f" AND ({op.join(parts)})", params

    # Try AND first
    and_sql, and_params = _kw_clauses(" AND ")
    return and_sql, and_params


@router.get("/search", response_model=SearchResult)
def search_datasets(
    q: str = "",
    category: Optional[List[str]] = Query(None),
    team: Optional[List[str]] = Query(None),
    topic: Optional[List[str]] = Query(None),
    category_id: Optional[int] = None,
    limit: int = 20,
    offset: int = 0,
):
    """Multi-filter dataset search. Logs the query to opendata.search_logs."""
    where = ["1=1"]
    params: list = []
    keywords = q.strip().split() if q else []

    # Text search — AND first; we'll detect zero-result and re-try with OR below.
    use_or_fallback = False
    if keywords:
        and_clauses = []
        for kw in keywords:
            and_clauses.append(
                "(d.title ILIKE %s OR d.description ILIKE %s OR d.tags ILIKE %s)"
            )
            like = f"%{kw}%"
            params.extend([like, like, like])
        where.append("(" + " AND ".join(and_clauses) + ")")

    # Category filter
    if category_id:
        where.append("d.category_id = %s")
        params.append(category_id)
    elif category:
        where.append(
            "d.category_id IN (SELECT id FROM opendata.categories WHERE name = ANY(%s))"
        )
        params.append(category)

    # Team filter (business_units.code → bu_id)
    if team:
        where.append(
            "d.bu_id IN (SELECT id FROM opendata.business_units WHERE code = ANY(%s))"
        )
        params.append(team)

    # Topic filter (matched against tags)
    if topic:
        topic_clauses = []
        for t in topic:
            topic_clauses.append("d.tags ILIKE %s")
            params.append(f"%{t}%")
        where.append("(" + " OR ".join(topic_clauses) + ")")

    where_sql = " WHERE " + " AND ".join(where)

    with get_conn() as conn:
        with conn.cursor() as cur:
            cur.execute(
                "SELECT COUNT(*) AS n FROM opendata.datasets d" + where_sql,
                params,
            )
            total = cur.fetchone()["n"]

            # If multi-keyword AND yielded nothing, fall back to OR
            if total == 0 and len(keywords) > 1:
                or_where = ["1=1"]
                or_params: list = []
                or_clauses = []
                for kw in keywords:
                    or_clauses.append(
                        "(d.title ILIKE %s OR d.description ILIKE %s OR d.tags ILIKE %s)"
                    )
                    like = f"%{kw}%"
                    or_params.extend([like, like, like])
                or_where.append("(" + " OR ".join(or_clauses) + ")")
                # Re-apply non-keyword filters
                if category_id:
                    or_where.append("d.category_id = %s")
                    or_params.append(category_id)
                elif category:
                    or_where.append(
                        "d.category_id IN (SELECT id FROM opendata.categories WHERE name = ANY(%s))"
                    )
                    or_params.append(category)
                if team:
                    or_where.append(
                        "d.bu_id IN (SELECT id FROM opendata.business_units WHERE code = ANY(%s))"
                    )
                    or_params.append(team)
                if topic:
                    tc = []
                    for t in topic:
                        tc.append("d.tags ILIKE %s")
                        or_params.append(f"%{t}%")
                    or_where.append("(" + " OR ".join(tc) + ")")
                where_sql = " WHERE " + " AND ".join(or_where)
                params = or_params
                cur.execute(
                    "SELECT COUNT(*) AS n FROM opendata.datasets d" + where_sql,
                    params,
                )
                total = cur.fetchone()["n"]
                use_or_fallback = True

            cur.execute(
                _BASE_SELECT
                + where_sql
                + " ORDER BY d.download_count DESC NULLS LAST, d.id LIMIT %s OFFSET %s",
                params + [limit, offset],
            )
            rows = cur.fetchall()

            # Best-effort: log the search (don't fail the request if logging breaks)
            try:
                cur.execute(
                    "INSERT INTO opendata.search_logs (query) VALUES (%s)",
                    (q or "",),
                )
                conn.commit()
            except Exception:
                conn.rollback()

    return SearchResult(total=total, datasets=[_row_to_dataset(r) for r in rows])
