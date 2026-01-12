from typing import Optional

from injector import Inject
from sqlalchemy import select
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.common.application.user_role import UserRole
from src.common.domain.value_objects.cedula import Cedula
from src.modules.users_management.application.hashing.hashing_provider import HashingProvider
from src.modules.users_management.application.interactors.login.credentials_query import CredentialsQuery
from src.modules.users_management.application.interactors.login.credentials_response import CredentialsResponse
from src.modules.users_management.application.interactors.login.credentials_service import CredentialsService
from src.modules.users_management.infrastructure.persistence.sqlalchemy.models.user_model import UserModel


class SqlAlchemyCredentialsService(CredentialsService):
    def __init__(
            self,
            async_session_factory: Inject[async_sessionmaker[AsyncSession]],
            hashing_provider: Inject[HashingProvider]
    ):
        self.__async_session_factory = async_session_factory
        self.__hashing_provider = hashing_provider

    async def execute_async(self, query: CredentialsQuery) -> Optional[CredentialsResponse]:
        async with (self.__async_session_factory() as session):
            statement = select(
                UserModel.id,
                UserModel.email,
                UserModel.password_hash,
                UserModel.is_admin,
                UserModel.psychologist_cedula
            ).where(UserModel.email == str(query.email)).fetch(1)

            result = (await session.execute(statement)).fetchone()

            if result is None:
                return None

            if (query.role == UserRole.ADMIN) ^ result.is_admin:
                return None

            if not self.__hashing_provider.verify_hash(query.password, result.password_hash):
                return None

            cedula: Optional[Cedula] = None if result.is_admin else Cedula(result.psychologist_cedula)

            return CredentialsResponse(
                id=result.id,
                cedula=cedula
            )
