import os

from fastapi import APIRouter, HTTPException, Security
from fastapi_injector import Injected
from mediatr import Mediator
from starlette.responses import JSONResponse

from src.common.domain.value_objects.email import Email
from src.modules.users_management.api.auth.login_dto import LoginDto
from src.modules.users_management.application.interactors.login.invalid_credentials_exception import \
    InvalidCredentialsException
from src.modules.users_management.application.interactors.login.login_command import LoginCommand
from src.common.infrastructure.token.access_security import access_security

router = APIRouter(prefix="/auth", tags=["auth"])


@router.post("/login")
async def login(login_dto: LoginDto, mediator: Mediator = Injected(Mediator)):
    command = LoginCommand(
        email=Email(login_dto.email),
        password=login_dto.password,
        role=login_dto.role
    )
    try:
        token = await mediator.send_async(command)
        response = JSONResponse(content={"accessToken": token})
        response.set_cookie(key="accessToken", value=token, httponly=True, secure=True,
                            samesite="none",
                            expires=int(os.getenv("ACCESS_TOKEN_EXPIRE_MINUTES")) * 60)
        return response
    except InvalidCredentialsException:
        raise HTTPException(status_code=401)


@router.post("/logout", dependencies=[Security(access_security)])
async def logout():
    response = JSONResponse(content=None)
    response.set_cookie(key="accessToken", value="", expires=0, httponly=True, secure=True,
                            samesite="none",)
    return response
