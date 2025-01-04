from fastapi import APIRouter

from api.routers import *

router = APIRouter()

router.include_router(user.router, tags=["users"], prefix="/user")
router.include_router(test.router, tags=["test"], prefix="/test")
router.include_router(restrictions.router, tags=["restrictions"], prefix="/restrictions")
router.include_router(files.router, prefix="/files", tags=["files"])
router.include_router(auth.router, prefix="/auth", tags=["auth"])
