from pydantic import BaseModel, ConfigDict, Field
from pydantic.alias_generators import to_camel

from src.common.domain.value_objects.sex import Sex


class AddPsychologistUserDto(BaseModel):
    model_config = ConfigDict(alias_generator=to_camel)

    cedula: str
    name: str
    sex: Sex = Field(max_length=1)
    email: str
    password: str
