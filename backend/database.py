from contextlib import contextmanager
from typing import Generator

import psycopg2
import psycopg2.extras

from config import (
    LAKEBASE_HOST,
    LAKEBASE_PORT,
    LAKEBASE_DATABASE,
    LAKEBASE_USER,
    LAKEBASE_PASSWORD,
)


def _connect() -> psycopg2.extensions.connection:
    return psycopg2.connect(
        host=LAKEBASE_HOST,
        port=LAKEBASE_PORT,
        dbname=LAKEBASE_DATABASE,
        user=LAKEBASE_USER,
        password=LAKEBASE_PASSWORD,
        cursor_factory=psycopg2.extras.RealDictCursor,
    )


@contextmanager
def get_conn() -> Generator[psycopg2.extensions.connection, None, None]:
    conn = _connect()
    try:
        yield conn
    finally:
        conn.close()
