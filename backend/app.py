import os

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import FileResponse

from config import MODE
from routers.genie import router as genie_router

app = FastAPI(title="Embedded Genie")

if MODE == "LOCAL":
    app.add_middleware(
        CORSMiddleware,
        allow_origins=["http://localhost:5173", "http://127.0.0.1:5173"],
        allow_methods=["GET"],
        allow_headers=["*"],
    )

app.include_router(genie_router)

_dist = os.path.realpath(
    os.path.join(os.path.dirname(os.path.abspath(__file__)), "..", "frontend", "dist")
)


@app.get("/{full_path:path}")
async def spa_fallback(full_path: str):
    """Serve static files; fall back to index.html for all SPA routes."""
    if os.path.isdir(_dist):
        candidate = os.path.realpath(os.path.join(_dist, full_path))
        if candidate.startswith(_dist) and os.path.isfile(candidate):
            return FileResponse(candidate)
        return FileResponse(os.path.join(_dist, "index.html"))
