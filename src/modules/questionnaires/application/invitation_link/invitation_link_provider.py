import os
from datetime import datetime, timedelta, timezone

import jwt

SECRET_KEY = os.getenv("INVITATION_LINK_SECRET_KEY")


class InvitationLinkProvider:
    @staticmethod
    def generate_token(test_session_id: int) -> str:
        payload = {
            "test_session_id": test_session_id,
            "exp": datetime.now(tz=timezone.utc) + timedelta(hours=1)
        }
        return jwt.encode(payload, SECRET_KEY, algorithm="HS256")

    @staticmethod
    def decode_token(token: str):
        try:
            return jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
        except jwt.ExpiredSignatureError:
            raise Exception("Token has expired")
        except jwt.InvalidTokenError:
            raise Exception("Invalid token")

    @staticmethod
    def validate_token(token: str) -> bool:
        try:
            jwt.decode(token, SECRET_KEY, algorithms=["HS256"])
            return True
        except jwt.InvalidTokenError:
            return False
