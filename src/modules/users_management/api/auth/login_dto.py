from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel

from src.common.application.user_role import UserRole


class LoginDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    role: UserRole
    email: str
    password: str
