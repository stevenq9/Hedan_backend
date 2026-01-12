from dataclasses import dataclass

from src.common.application.command import Command
from src.common.application.user_role import UserRole
from src.common.domain.value_objects.email import Email


@dataclass(frozen=True)
class LoginCommand(Command[str]):
    email: Email
    password: str
    role: UserRole
