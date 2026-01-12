import os
from datetime import timedelta

from fastapi_jwt import JwtAccessBearer

access_expires_delta = timedelta(minutes=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")))
refresh_expires_delta=timedelta(minutes=int(os.getenv("REFRESH_TOKEN_EXPIRE_MINUTES")))

access_security = JwtAccessBearer(
    secret_key=os.getenv("JWT_AUTH_SECRET_KEY"),
    auto_error=True,
    algorithm="HS256",
    access_expires_delta=access_expires_delta,
    refresh_expires_delta=refresh_expires_delta
)
