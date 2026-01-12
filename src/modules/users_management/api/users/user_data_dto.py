from typing import Optional

from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class UserDataDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    cedula: Optional[str]
    role: str
