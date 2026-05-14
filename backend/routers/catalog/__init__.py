"""Catalog routers — datasets, categories, business units, search, data access.

All routes mounted under the same /api prefix as routers.genie so the SPA can call
/api/categories, /api/search, /api/data/datasets/{id}/preview, etc.
"""
from fastapi import APIRouter

from . import business_units, categories, data_access, datasets, search

router = APIRouter(prefix="/api")
router.include_router(categories.router)
router.include_router(datasets.router)
router.include_router(search.router)
router.include_router(business_units.router)
router.include_router(data_access.router)
