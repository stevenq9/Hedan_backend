from dataclasses import dataclass
from typing import Optional

from src.common.application.query import Query
from src.common.application.user_role import UserRole
from src.common.domain.value_objects.email import Email
from src.modules.users_management.application.interactors.login.credentials_response import CredentialsResponse


@dataclass(frozen=True)
class CredentialsQuery(Query[Optional[CredentialsResponse]]):
    email: Email
    password: str
    role: UserRole
