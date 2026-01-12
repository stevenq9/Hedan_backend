from typing import List

from fastapi import APIRouter

from src.modules.users_management.api.auth.auth_router import router as auth_router
from src.modules.users_management.api.users.user_router import router as user_router

routers: List[APIRouter] = [
    auth_router,
    user_router
]
