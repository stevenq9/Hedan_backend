from injector import Inject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.users_management.application.hashing.hashing_provider import HashingProvider
from src.modules.users_management.application.interactors.add_psychologist_user.add_psychologist_user_command import \
    AddPsychologistUserCommand
from src.modules.users_management.application.interactors.add_psychologist_user.create_psychologist_user_service import \
    CreatePsychologistUserService
from src.modules.users_management.infrastructure.persistence.sqlalchemy.models.user_model import UserModel


class SqlAlchemyCreatePsychologistUserService(CreatePsychologistUserService):
    def __init__(
            self,
            async_session_factory: Inject[async_sessionmaker[AsyncSession]],
            hashing_provider: Inject[HashingProvider]
    ):
        self.__async_session_factory = async_session_factory
        self.__hashing_provider = hashing_provider

    async def execute_async(self, query: AddPsychologistUserCommand) -> None:
        user_model = UserModel(
            email=str(query.email),
            password_hash=self.__hashing_provider.generate_hash(query.password),
            is_admin=False,
            psychologist_cedula=str(query.cedula)
        )

        async with self.__async_session_factory() as session:
            session.add(user_model)
            await session.commit()
