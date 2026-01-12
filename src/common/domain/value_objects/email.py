import re
from dataclasses import dataclass

from src.common.domain.value_object import ValueObject


@dataclass(frozen=True)
class Email(ValueObject):
    email_address: str

    def __post_init__(self):
        if not Email.is_valid(self.email_address):
            raise ValueError(f"Invalid email address: {self.email_address}")

    def __str__(self):
        return self.email_address

    @property
    def domain(self) -> str:
        return self.email_address.split("@")[1]

    @classmethod
    def is_valid(cls, email_address: str) -> bool:
        email_regex = re.compile(
            r"(^[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+$)"
        )
        return re.match(email_regex, email_address) is not None
