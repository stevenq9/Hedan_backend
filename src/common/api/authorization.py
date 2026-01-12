from fastapi import Security, HTTPException
from fastapi_jwt import JwtAuthorizationCredentials

from src.common.application.user_role import UserRole
from src.common.infrastructure.token.access_security import access_security


def admin_only(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if credentials["role"] != UserRole.ADMIN:
        raise HTTPException(status_code=403, detail="Admin role is required")


def psychologist_only(credentials: JwtAuthorizationCredentials = Security(access_security)):
    if credentials["role"] != UserRole.PSYCHOLOGIST:
        raise HTTPException(status_code=403, detail="Psychologist role is required")


def psychologist_with_cedula(psychologist_cedula: str,
                             credentials: JwtAuthorizationCredentials = Security(access_security)):
    psychologist_only(credentials)

    if credentials["cedula"] != psychologist_cedula:
        raise HTTPException(status_code=403, detail="Unauthorizated cedula to access")


def psychologist_with_cedula_or_admin(psychologist_cedula: str,
                                      credentials: JwtAuthorizationCredentials = Security(access_security)):
    if credentials["role"] == UserRole.ADMIN:
        return

    psychologist_with_cedula(psychologist_cedula, credentials)
