from injector import Inject
from sqlalchemy.ext.asyncio import async_sessionmaker, AsyncSession

from src.modules.patients.domain.child.child import Child
from src.modules.patients.domain.child.child_repository_async import ChildRepositoryAsync
from src.modules.patients.infrastructure.persistence.sqlalchemy.models.child_model import ChildModel


class SqlAlchemyChildRepositoryAsync(ChildRepositoryAsync):
    def __init__(self, async_session_factory: Inject[async_sessionmaker[AsyncSession]]):
        self.__async_session_factory = async_session_factory

    async def add_child(self, child: Child) -> int:
        child_model = ChildModel(
            name=child.name,
            sex=str(child.sex),
            birthdate=child.birthdate,
            scholar_grade=int(child.scholar_grade),
            psychologist_cedula=str(child.psychologist_cedula),
        )

        async with self.__async_session_factory() as session:
            session.add(child_model)
            await session.commit()
            return child_model.id
