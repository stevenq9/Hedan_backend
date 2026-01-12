from abc import ABC, abstractmethod

from src.modules.users_management.application.token.token_payload import TokenPayload


class TokenProvider(ABC):
    @abstractmethod
    def generate_token(self, token_payload: TokenPayload) -> str:
        ...

    @abstractmethod
    def validate_token(self, token: str) -> bool:
        ...
