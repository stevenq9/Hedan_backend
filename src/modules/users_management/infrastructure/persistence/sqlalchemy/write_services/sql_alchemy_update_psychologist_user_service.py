# sql_alchemy_update_psychologist_user_service.py
from injector import Inject
from sqlalchemy import select
from sqlalchemy.exc import NoResultFound
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession
from sqlalchemy.future import select as future_select

from src.modules.users_management.application.hashing.hashing_provider import HashingProvider
from src.modules.users_management.application.interactors.update_psychologist_user.update_psychologist_user_command import \
    UpdatePsychologistUserCommand
from src.modules.users_management.application.interactors.update_psychologist_user.update_psychologist_user_service import \
    UpdatePsychologistUserService
from src.modules.users_management.infrastructure.persistence.sqlalchemy.models.user_model import UserModel


class SqlAlchemyUpdatePsychologistUserService(UpdatePsychologistUserService):
    def __init__(
            self,
            async_session_factory: Inject[async_sessionmaker[AsyncSession]],
            hashing_provider: Inject[HashingProvider]
    ):
        self.__async_session_factory = async_session_factory
        self.__hashing_provider = hashing_provider

    async def execute_async(self, command: UpdatePsychologistUserCommand) -> None:
        async with self.__async_session_factory() as session:
            try:
                # Query for the user associated with the psychologist
                user_query = select(UserModel).where(UserModel.psychologist_cedula == str(command.cedula))
                user_result = await session.execute(user_query)
                user = user_result.scalar_one()
                user.email = str(command.email)
                if command.change_password:
                    user.password_hash = self.__hashing_provider.generate_hash(command.password)


                # Commit the transaction
                await session.commit()

            except NoResultFound:
                # Handle case where either psychologist or user is not found
                raise ValueError("Psychologist or User not found")

            except Exception as e:
                # Rollback in case of any other exception
                await session.rollback()
                raise e