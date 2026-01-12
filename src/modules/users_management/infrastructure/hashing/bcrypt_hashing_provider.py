import bcrypt

from src.modules.users_management.application.hashing.hashing_provider import HashingProvider


class BCryptHashingProvider(HashingProvider):
    def generate_hash(self, value: str, salt: str = "") -> str:
        return (bcrypt.hashpw(value.encode("utf-8"), bcrypt.gensalt())).decode("utf-8")

    def verify_hash(self, value: str, hashed_value: str, salt: str = "") -> bool:
        return bcrypt.checkpw(value.encode("utf-8"), hashed_value.encode("utf-8"))
