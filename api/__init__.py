from fastapi import APIRouter
from api.users import router as user_router
from api.tests import router as test_router

router = APIRouter()
router.include_router(user_router)
router.include_router(test_router)
