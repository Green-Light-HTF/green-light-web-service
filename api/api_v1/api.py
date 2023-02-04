from fastapi import APIRouter

from .endpoints.api_endpoints import router as main_router

router = APIRouter()
router.include_router(main_router)
