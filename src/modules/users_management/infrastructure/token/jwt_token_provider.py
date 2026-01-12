from src.common.infrastructure.token.access_security import access_security, access_expires_delta
from src.modules.users_management.application.token.token_payload import TokenPayload
from src.modules.users_management.application.token.token_provider import TokenProvider


class JwtTokenProvider(TokenProvider):

    def generate_token(self, token_payload: TokenPayload) -> str:
        subject = {
            "user_id": token_payload.id,
            "role": token_payload.role
        }
        if token_payload.cedula is not None:
            subject["cedula"] = str(token_payload.cedula)

        return access_security.create_access_token(
            subject=subject,
            expires_delta=access_expires_delta
        )

    def validate_token(self, token: str) -> bool:
        ...