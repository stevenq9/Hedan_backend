from pydantic import BaseModel, ConfigDict
from pydantic.alias_generators import to_camel


class ValidateTokenDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    token: str
