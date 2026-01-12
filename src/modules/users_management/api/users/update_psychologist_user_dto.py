from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.common.domain.value_objects.cedula import Cedula
from src.common.domain.value_objects.email import Email
from src.common.domain.value_objects.sex import Sex


class UpdatePsychologistUserDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    name: str = Field(max_length=100)
    sex: Sex = Field(max_length=1)
    email: str
    password: str
    change_password: bool
