from abc import ABC, abstractmethod


class HashingProvider(ABC):
    @abstractmethod
    def generate_hash(self, value: str, salt: str = "") -> str:
        ...

    @abstractmethod
    def verify_hash(self, value: str, hashed_value: str, salt: str = "") -> bool:
        ...
