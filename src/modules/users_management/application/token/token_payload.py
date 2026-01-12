from dataclasses import dataclass
from typing import Optional

from src.common.application.user_role import UserRole
from src.common.domain.value_objects.cedula import Cedula


@dataclass(frozen=True)
class TokenPayload:
    id: int
    role: UserRole
    cedula: Optional[Cedula]
