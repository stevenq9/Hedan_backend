from typing import Optional

from injector import Inject

from src.common.application.command_handler import CommandHandler
from src.modules.users_management.application.interactors.login.credentials_query import CredentialsQuery
from src.modules.users_management.application.interactors.login.credentials_response import CredentialsResponse
from src.modules.users_management.application.interactors.login.credentials_service import CredentialsService
from src.modules.users_management.application.interactors.login.invalid_credentials_exception import \
    InvalidCredentialsException
from src.modules.users_management.application.interactors.login.login_command import LoginCommand
from src.modules.users_management.application.token.token_payload import TokenPayload
from src.modules.users_management.application.token.token_provider import TokenProvider


class LoginCommandHandler(CommandHandler[LoginCommand, str]):
    def __init__(
            self,
            credentials_service: Inject[CredentialsService],
            token_provider: Inject[TokenProvider]
    ):
        self.__credentials_service = credentials_service
        self.__token_provider = token_provider

    async def handle(self, command: LoginCommand) -> str:
        credentials_query = CredentialsQuery(
            email=command.email,
            password=command.password,
            role=command.role
        )

        credentials_response: Optional[CredentialsResponse] = await self.__credentials_service.execute_async(credentials_query)
        if credentials_response is None:
            raise InvalidCredentialsException()

        return self.__token_provider.generate_token(TokenPayload(
            id=credentials_response.id,
            role=command.role,
            cedula=credentials_response.cedula
        ))
