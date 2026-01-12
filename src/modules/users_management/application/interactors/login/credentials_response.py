from typing import Optional

from pydantic.dataclasses import dataclass

from src.common.domain.value_objects.cedula import Cedula


@dataclass(frozen=True)
class CredentialsResponse:
    id: int
    cedula: Optional[Cedula]
