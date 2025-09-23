from fastapi import APIRouter
from .auth import router as auth_router
from .data import router as data_router
from .api import router as scheduler_router
from .drop import router as drop_router

router = APIRouter()
router.include_router(auth_router)
router.include_router(data_router)
router.include_router(scheduler_router)
router.include_router(drop_router)
