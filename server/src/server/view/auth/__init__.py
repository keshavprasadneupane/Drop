from fastapi import APIRouter

from .login import router as login_router
from .register import router as register_router
from .user import router as user_router

auth_router = APIRouter(
    prefix="/auth",
    tags=["Authentication"],
)

# # registering all routers for authentication endpoints
auth_router.include_router(login_router)
auth_router.include_router(register_router)
auth_router.include_router(user_router)