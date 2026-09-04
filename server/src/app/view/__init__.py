from .auth import auth_router

from fastapi import APIRouter

routers = APIRouter()

routers.include_router(auth_router)
# example of how to include other routers if needed
#routers.include_router(another_router)
#routers.include_router(another_router1)
#routers.include_router(another_router2)