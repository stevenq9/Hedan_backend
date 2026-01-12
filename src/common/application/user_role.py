from enum import Enum


class UserRole(str, Enum):
    ADMIN = "admin"
    PSYCHOLOGIST = "psychologist"

    def __str__(self):
        return str(self.value)
